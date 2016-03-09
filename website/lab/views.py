from django.http import HttpResponse
from django.template import loader
import json
from .models import News
from django.utils import timezone

# Create your views here.


def custom_404(request):
    data = json.dumps({
        'status': 'error',
        'message': '404 Page not found'
    })
    return HttpResponse(data, content_type='application/json')


def news(request):
    objects = News.objects.all()
    data = []
    now = timezone.now()
    for object in objects:
        if object.visible_from_date < now < object.visible_till_date:
            data.append({
                'title': object.title,
                'description': object.description,
                'link': object.link
            })
    return HttpResponse(json.dumps(data), content_type='application/json')


def index(request):
    template = loader.get_template('serc/index.html')
    context = {
        'site_title': 'SERC'
    }
    return HttpResponse(template.render(context, request))