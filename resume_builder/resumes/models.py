from django.db import models


# ──────────────────────────────────────────────
# Main Resume Model
# ──────────────────────────────────────────────
class Resume(models.Model):
    # Personal Information
    full_name = models.CharField(max_length=100)
    professional_title = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    # Professional Summary
    professional_summary = models.TextField(blank=True)

    # Target Job
    job_description = models.TextField(blank=True, null=True)

    # AI Output
    ai_generated_resume = models.TextField(blank=True, null=True)
    ats_score = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


# ──────────────────────────────────────────────
# Resume Version Tracking
# ──────────────────────────────────────────────
class ResumeVersion(models.Model):
    resume = models.ForeignKey(Resume, related_name='versions', on_delete=models.CASCADE)
    version_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.pk} - {self.resume.full_name}"


# ──────────────────────────────────────────────
# Education
# ──────────────────────────────────────────────
GRADE_TYPE_CHOICES = [
    ('CGPA', 'CGPA'),
    ('Percentage', 'Percentage'),
    ('GPA', 'GPA'),
    ('Grade', 'Grade'),
]


class Education(models.Model):
    resume = models.ForeignKey(Resume, related_name='educations', on_delete=models.CASCADE)
    degree = models.CharField(max_length=100, help_text="e.g. Bachelor's Degree, Diploma, 12th")
    field_of_study = models.CharField(max_length=150, blank=True, help_text="e.g. Computer Science, Commerce")
    institution = models.CharField(max_length=200)
    board_university = models.CharField(max_length=200, blank=True, help_text="e.g. CBSE, Gujarat University")
    start_year = models.CharField(max_length=10, blank=True)
    end_year = models.CharField(max_length=10, blank=True, help_text="e.g. 2023 or Present")
    currently_studying = models.BooleanField(default=False)
    grade = models.CharField(max_length=50, blank=True, help_text="e.g. 8.47 or 85")
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPE_CHOICES, blank=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, help_text="Additional details about coursework, honors, etc.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.degree} - {self.institution}"


# ──────────────────────────────────────────────
# Experience
# ──────────────────────────────────────────────
EMPLOYMENT_TYPE_CHOICES = [
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
    ('Internship', 'Internship'),
    ('Freelance', 'Freelance'),
    ('Contract', 'Contract'),
]


class Experience(models.Model):
    resume = models.ForeignKey(Resume, related_name='experiences', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, blank=True)
    start_date = models.CharField(max_length=20, blank=True, help_text="e.g. Jan 2024")
    end_date = models.CharField(max_length=20, blank=True, help_text="e.g. Present")
    currently_working = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, help_text="One bullet point per line")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


# ──────────────────────────────────────────────
# Projects
# ──────────────────────────────────────────────
class Project(models.Model):
    resume = models.ForeignKey(Resume, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    technologies = models.TextField(blank=True, help_text="Comma-separated: Django, Python, SQLite")
    github_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)
    start_date = models.CharField(max_length=20, blank=True, help_text="e.g. Jan 2025")
    end_date = models.CharField(max_length=20, blank=True, help_text="e.g. Mar 2025")
    description = models.TextField(blank=True, help_text="One bullet point per line")
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
# Skills
# ──────────────────────────────────────────────
SKILL_CATEGORY_CHOICES = [
    ('Programming Languages', 'Programming Languages'),
    ('Frameworks/Libraries', 'Frameworks/Libraries'),
    ('Web Technologies', 'Web Technologies'),
    ('Databases', 'Databases'),
    ('Tools', 'Tools'),
    ('AI/ML', 'AI/ML'),
    ('Soft Skills', 'Soft Skills'),
    ('Other', 'Other'),
]


class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=SKILL_CATEGORY_CHOICES)
    name = models.CharField(max_length=100, help_text="e.g. Python, React, Leadership")

    class Meta:
        ordering = ['category', 'id']

    def __str__(self):
        return f"{self.category}: {self.name}"


# ──────────────────────────────────────────────
# Certifications
# ──────────────────────────────────────────────
class Certification(models.Model):
    resume = models.ForeignKey(Resume, related_name='certifications', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200, blank=True)
    issue_date = models.CharField(max_length=20, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    certificate_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
# Achievements
# ──────────────────────────────────────────────
class Achievement(models.Model):
    resume = models.ForeignKey(Resume, related_name='achievements', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    date = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
# Extra-Curricular Activities
# ──────────────────────────────────────────────
class Activity(models.Model):
    resume = models.ForeignKey(Resume, related_name='activities', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    date = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
# Languages Known
# ──────────────────────────────────────────────
PROFICIENCY_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Fluent', 'Fluent'),
    ('Native', 'Native'),
]


class Language(models.Model):
    resume = models.ForeignKey(Resume, related_name='languages', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} ({self.proficiency})"


# ──────────────────────────────────────────────
# Interests / Hobbies
# ──────────────────────────────────────────────
class Interest(models.Model):
    resume = models.ForeignKey(Resume, related_name='interests', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
# Social Links
# ──────────────────────────────────────────────
PLATFORM_CHOICES = [
    ('LinkedIn', 'LinkedIn'),
    ('GitHub', 'GitHub'),
    ('LeetCode', 'LeetCode'),
    ('CodeChef', 'CodeChef'),
    ('HackerRank', 'HackerRank'),
    ('Twitter/X', 'Twitter/X'),
    ('Behance', 'Behance'),
    ('Dribbble', 'Dribbble'),
    ('Other', 'Other'),
]


class SocialLink(models.Model):
    resume = models.ForeignKey(Resume, related_name='social_links', on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.platform}: {self.url}"
