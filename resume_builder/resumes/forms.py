from django import forms
from django.forms import inlineformset_factory
from .models import (
    Resume, Education, Experience, Project, Skill,
    Certification, Achievement, Activity, Language, Interest, SocialLink,
)

JOB_ROLE_CHOICES = [
    ('', 'Select a Job Role'),
    ('Software Engineer', 'Software Engineer'),
    ('Frontend Developer', 'Frontend Developer'),
    ('Backend Developer', 'Backend Developer'),
    ('Full-Stack Developer', 'Full-Stack Developer'),
    ('Data Analyst', 'Data Analyst'),
    ('Data Scientist', 'Data Scientist'),
    ('Machine Learning Engineer', 'Machine Learning Engineer'),
    ('DevOps Engineer', 'DevOps Engineer'),
    ('Cloud Engineer', 'Cloud Engineer'),
    ('Product Manager', 'Product Manager'),
    ('UI/UX Designer', 'UI/UX Designer'),
    ('Marketing Specialist', 'Marketing Specialist'),
    ('Sales Representative', 'Sales Representative'),
    ('Customer Support', 'Customer Support'),
    ('Graphic Designer', 'Graphic Designer'),
    ('Project Manager', 'Project Manager'),
    ('Business Analyst', 'Business Analyst'),
    ('Cybersecurity Analyst', 'Cybersecurity Analyst'),
    ('Mobile App Developer', 'Mobile App Developer'),
    ('Other', 'Other'),
]


# ──────────────────────────────────────────────
# Main Resume Form
# ──────────────────────────────────────────────
class ResumeForm(forms.ModelForm):
    job_description = forms.ChoiceField(
        choices=JOB_ROLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'w-full'})
    )

    class Meta:
        model = Resume
        fields = [
            'full_name', 'professional_title', 'email', 'phone',
            'city', 'state', 'country',
            'linkedin', 'github', 'portfolio_url', 'profile_photo',
            'professional_summary', 'job_description',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. John Doe'}),
            'professional_title': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Full-Stack Developer'}),
            'email': forms.EmailInput(attrs={'class': 'w-full', 'placeholder': 'e.g. john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. +91 9876543210'}),
            'city': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Vadodara'}),
            'state': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Gujarat'}),
            'country': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. India'}),
            'linkedin': forms.URLInput(attrs={'class': 'w-full', 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': 'w-full', 'placeholder': 'https://github.com/...'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'w-full', 'placeholder': 'https://portfolio.dev'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'w-full', 'accept': 'image/*'}),
            'professional_summary': forms.Textarea(attrs={
                'class': 'w-full', 'rows': 4,
                'placeholder': 'Write a brief professional summary or career objective...'
            }),
        }


# ──────────────────────────────────────────────
# Education Form
# ──────────────────────────────────────────────
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            'degree', 'field_of_study', 'institution', 'board_university',
            'start_year', 'end_year', 'currently_studying',
            'grade', 'grade_type', 'location', 'description', 'order',
        ]
        widgets = {
            'degree': forms.TextInput(attrs={'class': 'w-full', 'placeholder': "e.g. Bachelor's Degree"}),
            'field_of_study': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Computer Science'}),
            'institution': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Parul University'}),
            'board_university': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Gujarat University'}),
            'start_year': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. 2019'}),
            'end_year': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. 2023 or Present'}),
            'currently_studying': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'grade': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. 8.47 or 85'}),
            'grade_type': forms.Select(attrs={'class': 'w-full'}),
            'location': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Vadodara, Gujarat'}),
            'description': forms.Textarea(attrs={'class': 'w-full', 'rows': 2, 'placeholder': 'Relevant coursework, honors, etc.'}),
            'order': forms.HiddenInput(),
        }


# ──────────────────────────────────────────────
# Experience Form
# ──────────────────────────────────────────────
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            'job_title', 'company_name', 'employment_type',
            'start_date', 'end_date', 'currently_working',
            'location', 'description', 'order',
        ]
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Software Developer'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Google'}),
            'employment_type': forms.Select(attrs={'class': 'w-full'}),
            'start_date': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Jan 2024'}),
            'end_date': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Present'}),
            'currently_working': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'location': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Bangalore, India'}),
            'description': forms.Textarea(attrs={
                'class': 'w-full', 'rows': 4,
                'placeholder': 'One bullet point per line:\n• Built REST APIs serving 10K+ users\n• Led team of 5 engineers'
            }),
            'order': forms.HiddenInput(),
        }


# ──────────────────────────────────────────────
# Project Form
# ──────────────────────────────────────────────
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'technologies', 'github_url', 'live_demo_url',
            'start_date', 'end_date', 'description', 'image', 'order',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. AI Resume Builder'}),
            'technologies': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'Django, Python, SQLite (comma separated)'}),
            'github_url': forms.URLInput(attrs={'class': 'w-full', 'placeholder': 'https://github.com/...'}),
            'live_demo_url': forms.URLInput(attrs={'class': 'w-full', 'placeholder': 'https://myapp.com'}),
            'start_date': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Jan 2025'}),
            'end_date': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Mar 2025'}),
            'description': forms.Textarea(attrs={
                'class': 'w-full', 'rows': 3,
                'placeholder': 'One bullet point per line:\n• Built a full-stack web app\n• Integrated AI for resume generation'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full', 'accept': 'image/*'}),
            'order': forms.HiddenInput(),
        }


# ──────────────────────────────────────────────
# Skill Form
# ──────────────────────────────────────────────
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'name']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full'}),
            'name': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Python, React, Leadership'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [('', 'Select Category')] + list(self.fields['category'].choices)


# ──────────────────────────────────────────────
# Certification Form
# ──────────────────────────────────────────────
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'issue_date', 'credential_id', 'certificate_url', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. AWS Solutions Architect'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Amazon Web Services'}),
            'issue_date': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Mar 2024'}),
            'credential_id': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. ABC123XYZ'}),
            'certificate_url': forms.URLInput(attrs={'class': 'w-full', 'placeholder': 'https://credential.net/...'}),
            'order': forms.HiddenInput(),
        }


# ──────────────────────────────────────────────
# Achievement Form
# ──────────────────────────────────────────────
class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'organization', 'date', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. 1st Place in Hackathon'}),
            'organization': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Google DevFest'}),
            'date': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Oct 2024'}),
            'description': forms.Textarea(attrs={'class': 'w-full', 'rows': 2, 'placeholder': 'Brief description...'}),
            'order': forms.HiddenInput(),
        }


# ──────────────────────────────────────────────
# Activity Form (Extra-Curricular)
# ──────────────────────────────────────────────
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'organization', 'date', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Event Coordinator'}),
            'organization': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. College Tech Club'}),
            'date': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. 2022-2023'}),
            'description': forms.Textarea(attrs={'class': 'w-full', 'rows': 2, 'placeholder': 'What you did and its impact...'}),
            'order': forms.HiddenInput(),
        }


# ──────────────────────────────────────────────
# Language Form
# ──────────────────────────────────────────────
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. English, Hindi'}),
            'proficiency': forms.Select(attrs={'class': 'w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proficiency'].choices = [('', 'Select Proficiency')] + list(self.fields['proficiency'].choices)


# ──────────────────────────────────────────────
# Interest Form
# ──────────────────────────────────────────────
class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full', 'placeholder': 'e.g. Open Source, Blogging, Chess'}),
        }


# ──────────────────────────────────────────────
# Social Link Form
# ──────────────────────────────────────────────
class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']
        widgets = {
            'platform': forms.Select(attrs={'class': 'w-full'}),
            'url': forms.URLInput(attrs={'class': 'w-full', 'placeholder': 'https://...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['platform'].choices = [('', 'Select Platform')] + list(self.fields['platform'].choices)


# ──────────────────────────────────────────────
# Inline Formsets
# ──────────────────────────────────────────────
EducationFormSet = inlineformset_factory(
    Resume, Education, form=EducationForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)

ExperienceFormSet = inlineformset_factory(
    Resume, Experience, form=ExperienceForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)

ProjectFormSet = inlineformset_factory(
    Resume, Project, form=ProjectForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)

SkillFormSet = inlineformset_factory(
    Resume, Skill, form=SkillForm,
    extra=3, can_delete=True, min_num=0, validate_min=False
)

CertificationFormSet = inlineformset_factory(
    Resume, Certification, form=CertificationForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)

AchievementFormSet = inlineformset_factory(
    Resume, Achievement, form=AchievementForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)

ActivityFormSet = inlineformset_factory(
    Resume, Activity, form=ActivityForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)

LanguageFormSet = inlineformset_factory(
    Resume, Language, form=LanguageForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)

InterestFormSet = inlineformset_factory(
    Resume, Interest, form=InterestForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)

SocialLinkFormSet = inlineformset_factory(
    Resume, SocialLink, form=SocialLinkForm,
    extra=1, can_delete=True, min_num=0, validate_min=False
)
