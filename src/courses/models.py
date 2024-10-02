from django.db import models


class PublishStatus(models.TextChoices):
        PUBLISHED = ('published', 'Published')
        COMING_SOON = ('coming soon', 'Coming Soon')
        DRAFT = ('draft', 'Draft')


class AccessRequirements(models.TextChoices):
     ANYONE = ('anyone', 'Anyone')
     EMAIL_REQUIRED = ('email required', 'Email Required')
     

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    access = models.CharField(max_length=20, choices=AccessRequirements.choices, default=AccessRequirements.ANYONE)
    image = models.ImageField()
    status = models.CharField(max_length=10, choices=PublishStatus.choices, default=PublishStatus.DRAFT)


    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED