from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    ResumeForm,
    EducationFormSet, ExperienceFormSet, ProjectFormSet, SkillFormSet,
    CertificationFormSet, AchievementFormSet, ActivityFormSet,
    LanguageFormSet, InterestFormSet, SocialLinkFormSet,
)
from .models import Resume, ResumeVersion
from . import ai_services
import json
import markdown
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO


# ──────────────────────────────────────────────
# Formset Configuration (prefix → FormSetClass)
# ──────────────────────────────────────────────
FORMSET_CONFIG = [
    ('education', EducationFormSet),
    ('experience', ExperienceFormSet),
    ('project', ProjectFormSet),
    ('skill', SkillFormSet),
    ('certification', CertificationFormSet),
    ('achievement', AchievementFormSet),
    ('activity', ActivityFormSet),
    ('language', LanguageFormSet),
    ('interest', InterestFormSet),
    ('social_link', SocialLinkFormSet),
]


def _build_formsets(request=None, instance=None):
    """Build all formsets for create or update views."""
    formsets = {}
    for prefix, FormSetClass in FORMSET_CONFIG:
        kwargs = {'prefix': prefix}
        if instance:
            kwargs['instance'] = instance
        if request:
            kwargs['data'] = request.POST
            kwargs['files'] = request.FILES
        formsets[prefix] = FormSetClass(**kwargs)
    return formsets


def _all_formsets_valid(formsets):
    """Check if every formset is valid."""
    return all(fs.is_valid() for fs in formsets.values())


def _save_all_formsets(formsets, resume):
    """Save all formsets to the given resume instance."""
    for fs in formsets.values():
        fs.instance = resume
        fs.save()


# ──────────────────────────────────────────────
# Format Helpers for AI Prompt
# ──────────────────────────────────────────────
def _format_education_text(resume):
    """Format education entries into a structured text string for the AI prompt."""
    educations = resume.educations.all()
    if not educations:
        return "Not specified"
    lines = []
    for edu in educations:
        parts = [edu.degree]
        if edu.field_of_study:
            parts[0] += f", {edu.field_of_study}"
        if edu.institution:
            parts.append(edu.institution)
        if edu.board_university:
            parts[-1] += f" ({edu.board_university})"
        if edu.location:
            parts[-1] += f", {edu.location}"
        if edu.start_year or edu.end_year:
            end = "Present" if edu.currently_studying else edu.end_year
            parts.append(f"{edu.start_year} - {end}")
        if edu.grade:
            grade_str = f"{edu.grade}"
            if edu.grade_type:
                grade_str += f" {edu.grade_type}"
            parts.append(f"Score: {grade_str}")
        if edu.description:
            parts.append(f"Details: {edu.description}")
        lines.append(" | ".join(parts))
    return "\n".join(lines)


def _format_experience_text(resume):
    """Format experience entries into a structured text string for the AI prompt."""
    experiences = resume.experiences.all()
    if not experiences:
        return "Not specified"
    lines = []
    for exp in experiences:
        parts = [f"Title: {exp.job_title}"]
        if exp.company_name:
            parts.append(f"Company: {exp.company_name}")
        if exp.employment_type:
            parts.append(f"Type: {exp.employment_type}")
        if exp.start_date or exp.end_date:
            end = "Present" if exp.currently_working else exp.end_date
            parts.append(f"Duration: {exp.start_date} - {end}")
        if exp.location:
            parts.append(f"Location: {exp.location}")
        if exp.description:
            parts.append(f"Description:\n{exp.description}")
        lines.append("\n".join(parts))
    return "\n---\n".join(lines)


def _format_projects_text(resume):
    """Format project entries into a structured text string for the AI prompt."""
    projects = resume.projects.all()
    if not projects:
        return ""
    lines = []
    for proj in projects:
        parts = [f"Project: {proj.title}"]
        if proj.start_date or proj.end_date:
            parts.append(f"Date: {proj.start_date} - {proj.end_date}")
        if proj.technologies:
            parts.append(f"Technologies: {proj.technologies}")
        if proj.description:
            parts.append(f"Description:\n{proj.description}")
        if proj.github_url:
            parts.append(f"GitHub: {proj.github_url}")
        if proj.live_demo_url:
            parts.append(f"Live Demo: {proj.live_demo_url}")
        lines.append("\n".join(parts))
    return "\n---\n".join(lines)


def _format_skills_text(resume):
    """Format skills by category for the AI prompt."""
    skills = resume.skills.all()
    if not skills:
        return "Not specified"
    categories = {}
    for skill in skills:
        categories.setdefault(skill.category, []).append(skill.name)
    lines = []
    for cat, names in categories.items():
        lines.append(f"{cat}: {', '.join(names)}")
    return "\n".join(lines)


def _format_certifications_text(resume):
    """Format certifications for the AI prompt."""
    certs = resume.certifications.all()
    if not certs:
        return ""
    lines = []
    for cert in certs:
        parts = [cert.name]
        if cert.issuing_organization:
            parts.append(f"by {cert.issuing_organization}")
        if cert.issue_date:
            parts.append(f"({cert.issue_date})")
        if cert.credential_id:
            parts.append(f"ID: {cert.credential_id}")
        lines.append(" — ".join(parts))
    return "\n".join(lines)


def _format_achievements_text(resume):
    """Format achievements for the AI prompt."""
    items = resume.achievements.all()
    if not items:
        return ""
    lines = []
    for item in items:
        parts = [item.title]
        if item.organization:
            parts.append(f"at {item.organization}")
        if item.date:
            parts.append(f"({item.date})")
        if item.description:
            parts.append(f"— {item.description}")
        lines.append(" ".join(parts))
    return "\n".join(lines)


def _format_activities_text(resume):
    """Format extra-curricular activities for the AI prompt."""
    items = resume.activities.all()
    if not items:
        return ""
    lines = []
    for item in items:
        parts = [item.title]
        if item.organization:
            parts.append(f"at {item.organization}")
        if item.date:
            parts.append(f"({item.date})")
        if item.description:
            parts.append(f"— {item.description}")
        lines.append(" ".join(parts))
    return "\n".join(lines)


def _format_languages_text(resume):
    """Format languages for the AI prompt."""
    langs = resume.languages.all()
    if not langs:
        return ""
    return ", ".join([f"{l.name} ({l.proficiency})" for l in langs])


def _format_interests_text(resume):
    """Format interests/hobbies for the AI prompt."""
    interests = resume.interests.all()
    if not interests:
        return ""
    return ", ".join([i.name for i in interests])


def _format_social_links_text(resume):
    """Format social links for the AI prompt."""
    links = resume.social_links.all()
    if not links:
        return ""
    return " | ".join([f"{link.platform}: {link.url}" for link in links])


def _build_contact_string(resume):
    """Build a formatted contact string from resume fields."""
    parts = [resume.email]
    if resume.phone:
        parts.append(resume.phone)
    location_parts = [p for p in [resume.city, resume.state, resume.country] if p]
    if location_parts:
        parts.append(", ".join(location_parts))
    if resume.linkedin:
        parts.append(resume.linkedin)
    if resume.github:
        parts.append(resume.github)
    if resume.portfolio_url:
        parts.append(resume.portfolio_url)
    return " | ".join(parts)


def _generate_and_save_ai_resume(resume):
    """Generate AI resume and analysis, and save to the resume instance."""
    # Format structured data for AI
    education_text = _format_education_text(resume)
    experience_text = _format_experience_text(resume)
    projects_text = _format_projects_text(resume)
    skills_text = _format_skills_text(resume)
    certifications_text = _format_certifications_text(resume)
    achievements_text = _format_achievements_text(resume)
    activities_text = _format_activities_text(resume)
    languages_text = _format_languages_text(resume)
    interests_text = _format_interests_text(resume)

    # Extract keywords from target job role
    keywords = ""
    if resume.job_description:
        keywords = ai_services.extract_keywords(resume.job_description)

    # Generate AI resume
    final_resume = ai_services.generate_resume(
        name=resume.full_name,
        professional_title=resume.professional_title,
        contact=_build_contact_string(resume),
        summary=resume.professional_summary,
        experience=experience_text,
        skills=skills_text,
        education=education_text,
        projects=projects_text,
        certifications=certifications_text,
        achievements=achievements_text,
        activities=activities_text,
        languages=languages_text,
        interests=interests_text,
        keywords=keywords,
    )

    # Analyze against job description
    analysis = ai_services.analyze_resume(final_resume, resume.job_description)

    resume.ai_generated_resume = final_resume
    resume.ats_score = analysis.get("ats_score", 0)
    resume.feedback = json.dumps({
        "strengths": analysis.get("strengths", []),
        "weaknesses": analysis.get("weaknesses", []),
        "missing_keywords": analysis.get("missing_keywords", []),
        "suggestions": analysis.get("suggestions", [])
    })
    resume.save()

    ResumeVersion.objects.create(
        resume=resume,
        version_text=final_resume
    )


# ──────────────────────────────────────────────
# Create Resume View
# ──────────────────────────────────────────────
def create_resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        formsets = _build_formsets(request)

        if form.is_valid() and _all_formsets_valid(formsets):
            resume = form.save()
            _save_all_formsets(formsets, resume)

            _generate_and_save_ai_resume(resume)

            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm()
        formsets = _build_formsets()

    return render(request, 'resumes/create_resume.html', {
        'form': form,
        **formsets,
    })


# ──────────────────────────────────────────────
# Resume List View
# ──────────────────────────────────────────────
def resume_list(request):
    resumes = Resume.objects.all().order_by('-created_at')

    for resume in resumes:
        if resume.feedback:
            try:
                resume.feedback_data = json.loads(resume.feedback)
            except Exception:
                resume.feedback_data = {}
        else:
            resume.feedback_data = {}

    return render(request, 'resumes/resume_list.html', {'resumes': resumes})


# ──────────────────────────────────────────────
# Update Resume View
# ──────────────────────────────────────────────
def update_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        formsets = _build_formsets(request, instance=resume)

        if form.is_valid() and _all_formsets_valid(formsets):
            resume = form.save()
            _save_all_formsets(formsets, resume)
            
            # Generate the new resume with updated details
            _generate_and_save_ai_resume(resume)
            
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(instance=resume)
        formsets = _build_formsets(instance=resume)

    return render(request, 'resumes/update_resume.html', {
        'form': form,
        'resume': resume,
        **formsets,
    })


# ──────────────────────────────────────────────
# Delete Resume View
# ──────────────────────────────────────────────
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == "POST":
        resume.delete()
        return redirect('resume_list')
    return render(request, 'resumes/delete_resume.html', {'resume': resume})


# ──────────────────────────────────────────────
# Resume Detail View
# ──────────────────────────────────────────────
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if resume.feedback:
        try:
            resume.feedback_data = json.loads(resume.feedback)
        except Exception:
            resume.feedback_data = {}
    else:
        resume.feedback_data = {}

    # Convert markdown resume to rendered HTML
    resume_html = ""
    if resume.ai_generated_resume:
        resume_html = markdown.markdown(resume.ai_generated_resume)

    return render(request, 'resumes/resume_detail.html', {'resume': resume, 'resume_html': resume_html})


# ──────────────────────────────────────────────
# PDF Download View
# ──────────────────────────────────────────────
def generate_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk)

    markdown_content = resume.ai_generated_resume or ("# " + resume.full_name + "\n\nNo AI resume generated yet.")

    # Convert markdown → HTML
    html_content = markdown.markdown(markdown_content)

    # Inject into template
    full_html = render_to_string("resumes/pdf_resume.html", {
        "content": html_content
    })

    # Generate PDF using xhtml2pdf
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(full_html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"{resume.full_name.replace(' ', '_')}_resume.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    return HttpResponse("Error generating PDF", status=500)
