from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    linkedin = models.URLField(blank=True, null=True)
    objective = models.TextField()
    skills = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    job_description = models.TextField(blank=True, null=True)
    ai_generated_resume = models.TextField(blank=True, null=True)
    ats_score = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ResumeVersion(models.Model):
    resume = models.ForeignKey(Resume, related_name='versions', on_delete=models.CASCADE)
    version_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
