from django.http import HttpResponse
from django.http import Http404
from django.template import loader
import json
from .models import News, Banner, SiteTextData, People, PeopleType, ShortNames, Publication, ConferenceType
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
    banners = Banner.objects.all().filter(is_active=True)
    text = SiteTextData.objects.all().filter(unique_identifier='homepage')
    now = timezone.now()
    news = News.objects.filter(visible_from_date__lte=now, visible_till_date__gte=now)
    context = {
        'PAGE_TITLE': 'Home',
        'banners': banners,
        'homepage': text[0].data,
        'news': news
    }
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template('serc/about.html')
    text = SiteTextData.objects.filter(unique_identifier='about_us')
    now = timezone.now()
    news = News.objects.filter(visible_from_date__lte=now, visible_till_date__gte=now)
    context = {
        'PAGE_TITLE': 'About',
        'about_us': text[0].data,
        'news': news
    }
    return HttpResponse(template.render(context, request))

def contact(request):
    template = loader.get_template('serc/contact.html')
    context = {
        'PAGE_TITLE': 'Contact',
    }
    return HttpResponse(template.render(context, request))

def service(request):
    template = loader.get_template('serc/service.html')
    text = SiteTextData.objects.filter(unique_identifier='about_us')
    now = timezone.now()
    news = News.objects.filter(visible_from_date__lte=now, visible_till_date__gte=now)
    context = {
        'PAGE_TITLE': 'Service',
        'about_us': text[0].data,
        'news': news
    }
    return HttpResponse(template.render(context, request))

def people(request, type):
    template = loader.get_template('serc/people.html')
    try:
        page_title = PeopleType.objects.filter(name=type)[0].display_text
    except:
        raise Http404
    types = PeopleType.objects.filter(name__startswith=type+'_').order_by('order')
    peoples = People.objects.filter(list_on__in=types)
    people_organized = {}
    for people in peoples:
        if people.list_on.display_text not in people_organized:
            people_organized[people.list_on.display_text] = []
        people_organized[people.list_on.display_text].append(people)
    context = {
        'PAGE_TITLE': page_title,
        'people_organized': people_organized
    }
    return HttpResponse(template.render(context, request))


def personal(request, name):
    template = loader.get_template('serc/personal.html')
    try:
        person_object = People.objects.filter(url=name)[0]
    except:
        raise Http404
    short_names = ShortNames.objects.filter(profile=person_object)
    publications = Publication.objects.filter(author__in=short_names)
    publications_organized = {}
    for publication in publications:
        if publication.conf_type.name not in publications_organized:
            publications_organized[publication.conf_type.name] = []
        publications_organized[publication.conf_type.name].append(publication)
    context = {
        'PAGE_TITLE': person_object.name,
        'person': person_object,
        'publications_organized': publications_organized
    }
    return HttpResponse(template.render(context, request))


def research(request):
    template = loader.get_template('serc/research.html')
    publications = Publication.objects.all()
    publications_organized = {}
    for publication in publications:
        if publication.conf_type.name not in publications_organized:
            publications_organized[publication.conf_type.name] = []
        publications_organized[publication.conf_type.name].append(publication)
    context = {
        'PAGE_TITLE': 'Research',
        'publications_organized': publications_organized
    }
    return HttpResponse(template.render(context, request))


def archive(request):
    template = loader.get_template('serc/archive.html')
    context = {
        'PAGE_TITLE': 'NEWS Archive',
        'news': News.objects.all()
    }
    return HttpResponse(template.render(context, request))