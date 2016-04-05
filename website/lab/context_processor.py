from django.template import RequestContext
from .models import PeopleType, SiteTextData, SocialIcon, ResourceType
from django.db.models import Q
from django.conf import settings

def sitetext(key):
    try:
        return SiteTextData.objects.filter(unique_identifier=key)[0].data
    except:
        return ""

def template_globals(request):
    people_dropdown = PeopleType.objects.filter(~Q(name__contains='_')).order_by('order')
    resource_dropdown = ResourceType.objects.all().order_by('order')
    return {
        "SITE_TITLE": "Software Engineering Research Center",
        "user": request.user,
        "people_dropdown": people_dropdown,
        "resource_dropdown": resource_dropdown,
        "copyright_text": sitetext('copyright_text'),
        "social": SocialIcon.objects.all(),
        "STATIC_URL": settings.STATIC_URL
    }