import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_builder.settings')
django.setup()

from resumes.forms import SkillForm
from django.forms import inlineformset_factory
from resumes.models import Resume, Skill

SkillFormSet = inlineformset_factory(Resume, Skill, form=SkillForm, extra=3, can_delete=True, min_num=0, validate_min=False)

# Simulate empty POST data for the extra forms
data = {
    'skill_set-TOTAL_FORMS': '3',
    'skill_set-INITIAL_FORMS': '0',
    'skill_set-MIN_NUM_FORMS': '0',
    'skill_set-MAX_NUM_FORMS': '1000',
    'skill_set-0-category': '',
    'skill_set-0-name': '',
    'skill_set-1-category': '',
    'skill_set-1-name': '',
    'skill_set-2-category': '',
    'skill_set-2-name': '',
}

formset = SkillFormSet(data=data)
print("Is valid?", formset.is_valid())
if not formset.is_valid():
    print("Errors:", formset.errors)
    print("Non form errors:", formset.non_form_errors())
