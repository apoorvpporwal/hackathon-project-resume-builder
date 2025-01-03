from django.db import models

# Create your models here.



# class Resume(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     linkedin = models.URLField(blank=True, null=True)
#     objective = models.TextField()
#     skills = models.TextField()  # Store a comma-separated list of skills
#     experience = models.TextField()  # Store experience details
#     education = models.TextField()  # Store education details
#     job_role = models.CharField(max_length=100)  # New field for job role
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    linkedin = models.URLField(blank=True, null=True)
    objective = models.TextField()
    skills = models.TextField()  # Store a comma-separated list of skills
    experience = models.TextField()  # Store experience details
    education = models.TextField()  # Store education details
    job_role = models.CharField(max_length=100)  # New field for job role
    ai_generated_resume = models.TextField(blank=True, null=True)  # New field for AI-generated resume
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name


