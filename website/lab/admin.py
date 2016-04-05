from django.contrib import admin
from .models import *
from django.utils import timezone
# Register your models here.

admin.site.register(News)
admin.site.register(Banner)
admin.site.register(SiteTextData)
admin.site.register(People)
admin.site.register(PeopleType)
admin.site.register(Publication)
admin.site.register(ConferenceType)
admin.site.register(ShortNames)
admin.site.register(SocialIcon)
admin.site.register(ResourceType)
