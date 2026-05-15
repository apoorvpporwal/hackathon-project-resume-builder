from django.contrib import admin
from .models import (
    Resume, ResumeVersion, Education, Experience, Project, Skill,
    Certification, Achievement, Activity, Language, Interest, SocialLink,
)


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 0


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 0


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0


class InterestInline(admin.TabularInline):
    model = Interest
    extra = 0


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0


class ResumeVersionInline(admin.TabularInline):
    model = ResumeVersion
    extra = 0
    readonly_fields = ('version_text', 'created_at')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'professional_title', 'email', 'ats_score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email')
    inlines = [
        EducationInline, ExperienceInline, ProjectInline, SkillInline,
        CertificationInline, AchievementInline, ActivityInline,
        LanguageInline, InterestInline, SocialLinkInline, ResumeVersionInline,
    ]


# Also register standalone for direct access
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Certification)
admin.site.register(Achievement)
admin.site.register(Activity)
admin.site.register(Language)
admin.site.register(Interest)
admin.site.register(SocialLink)
admin.site.register(ResumeVersion)
