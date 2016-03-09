from __future__ import unicode_literals

from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    created_date = models.DateTimeField(auto_now=True)
    visible_from_date = models.DateTimeField()
    visible_till_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def is_visible(self):
        current_time = timezone.now()
        return current_time > self.visible_from_date and current_time < self.visible_till_date

class Banner(models.Model):
    img = models.ImageField(upload_to='static/images/banners')
    is_active = models.BooleanField()

