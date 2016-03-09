from django.template import RequestContext
def template_globals(request):
    return {
        "SITE_TITLE": "Software Engineering Research Center",
        "user": request.user
    }