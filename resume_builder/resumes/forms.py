from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'email', 'phone', 'linkedin', 'objective', 'skills', 'experience', 'education', 'job_role']
