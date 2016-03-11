from django.template import RequestContext
from .models import PeopleType
from django.db.models import Q
def template_globals(request):
    people_dropdown = PeopleType.objects.filter(~Q(name__contains='_')).order_by('order')
    return {
        "SITE_TITLE": "Software Engineering Research Center",
        "user": request.user,
        "people_dropdown": people_dropdown
    }