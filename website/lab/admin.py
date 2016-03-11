from django.contrib import admin
from .models import News, Banner, SiteTextData, PeopleType, People, Publication, ConferenceType, ShortNames
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