from django import forms
from .models import Resume

JOB_ROLE_CHOICES = [
    ('', 'Select a Job Role'),
    ('Software Engineer', 'Software Engineer'),
    ('Data Analyst', 'Data Analyst'),
    ('Data Scientist', 'Data Scientist'),
    ('Product Manager', 'Product Manager'),
    ('Marketing Specialist', 'Marketing Specialist'),
    ('Sales Representative', 'Sales Representative'),
    ('Customer Support', 'Customer Support'),
    ('Graphic Designer', 'Graphic Designer'),
    ('Project Manager', 'Project Manager'),
    ('Other', 'Other'),
]

OBJECTIVE_CHOICES = [
    ('', 'Select an Objective'),
    ('Seeking an entry-level position to kickstart my career.', 'Seeking an entry-level position to kickstart my career.'),
    ('Looking to leverage my existing skills in a challenging environment.', 'Looking to leverage my existing skills in a challenging environment.'),
    ('Aiming to lead and manage cross-functional teams to drive success.', 'Aiming to lead and manage cross-functional teams to drive success.'),
    ('Transitioning into a new industry and eager to apply my transferable skills.', 'Transitioning into a new industry and eager to apply my transferable skills.'),
]

EDUCATION_CHOICES = [
    ('', 'Select Education Level'),
    ('High School Diploma', 'High School Diploma'),
    ('Associate Degree', 'Associate Degree'),
    ('Bachelor\'s Degree', 'Bachelor\'s Degree'),
    ('Master\'s Degree', 'Master\'s Degree'),
    ('Doctorate (Ph.D.)', 'Doctorate (Ph.D.)'),
    ('Bootcamp / Certification', 'Bootcamp / Certification'),
]

class ResumeForm(forms.ModelForm):
    job_description = forms.ChoiceField(
        choices=JOB_ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'w-full'})
    )
    objective = forms.ChoiceField(
        choices=OBJECTIVE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'w-full'})
    )
    education = forms.ChoiceField(
        choices=EDUCATION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'w-full'})
    )
    
    class Meta:
        model = Resume
        fields = ['name', 'email', 'phone', 'linkedin', 'objective', 'skills', 'experience', 'education', 'job_description']
