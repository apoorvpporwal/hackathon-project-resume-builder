from django.shortcuts import render, redirect, get_object_or_404
from .forms import ResumeForm
from .models import Resume, ResumeVersion
from . import ai_services
import json

def create_resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            
            keywords = ""
            if resume.job_description:
                keywords = ai_services.extract_keywords(resume.job_description)
                
            enhanced_experience = ai_services.enhance_experience(resume.experience)
            optimized_skills = ai_services.optimize_skills(resume.skills)
            
            final_resume = ai_services.generate_resume(
                name=resume.name,
                contact=f"{resume.email} | {resume.phone} | {resume.linkedin}",
                objective=resume.objective,
                enhanced_experience=enhanced_experience,
                optimized_skills=optimized_skills,
                education=resume.education,
                keywords=keywords
            )
            
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
            
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm()
    return render(request, 'resumes/create_resume.html', {'form': form})

def resume_list(request):
    resumes = Resume.objects.all().order_by('-created_at')
    
    # Parse the feedback JSON here so templates can iterate over it cleanly
    for resume in resumes:
        if resume.feedback:
            try:
                resume.feedback_data = json.loads(resume.feedback)
            except:
                resume.feedback_data = {}
        else:
            resume.feedback_data = {}
            
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

def update_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('resume_list')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resumes/update_resume.html', {'form': form, 'resume': resume})

def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == "POST":
        resume.delete()
        return redirect('resume_list')
    return render(request, 'resumes/delete_resume.html', {'resume': resume})

def resume_detail(request, pk):
    # Depending on active routing, keep this functional
    resume = get_object_or_404(Resume, pk=pk)
    if resume.feedback:
        try:
            resume.feedback_data = json.loads(resume.feedback)
        except:
            resume.feedback_data = {}
    else:
        resume.feedback_data = {}
    return render(request, 'resumes/resume_detail.html', {'resume': resume})
import markdown
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO

def generate_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk)

    markdown_content = resume.ai_generated_resume or ("# " + resume.name + "\n\nNo AI resume generated yet.")

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
        filename = f"{resume.name.replace(' ', '_')}_resume.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse("Error generating PDF", status=500)
