from django.contrib import admin
from .models import News, Banner
from django.utils import timezone
# Register your models here.

admin.site.register(News)
admin.site.register(Banner)