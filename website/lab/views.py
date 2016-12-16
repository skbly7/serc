from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
import json
from calendarium import views as calendar_views
from .models import News, Banner, SiteTextData, People, PeopleType, ShortNames, Publication, ConferenceType, ShortNamePublicationMapping, ResourceType
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.db import connections, transaction
from django.core.cache import cache
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from .forms import ContactForm
from collections import OrderedDict

# Create your views here.


def custom_404(request):
    data = json.dumps({
        'status': 'error',
        'message': '404 Page not found'
    })
    return HttpResponse(data, content_type='application/json')

@cache_page(60)
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

@cache_page(60)
def index(request):
    template = loader.get_template('lab/index.html')
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

@cache_page(60)
def people(request, type):
    template = loader.get_template('lab/people.html')
    try:
        page_title = PeopleType.objects.filter(name=type)[0].display_text
    except:
        raise Http404
    context = {
        'PAGE_TITLE': page_title,
        'people_organized': people_organized_call(type)
    }
    return HttpResponse(template.render(context, request))

def people_organized_call(type):
    types = PeopleType.objects.filter(name__startswith=type+'_').order_by('-order')
    peoples = People.objects.filter(list_on__in=types).order_by('-display_priority')
    people_organized = OrderedDict()
    for type in types:
        people_organized[type.display_text] = []
    for people in peoples:
        if not people.list_on.show_research_interest:
            people.interest = ""
        people.count_in_one_row = people.list_on.count_in_one_row
        people_organized[people.list_on.display_text].append(people)
    for type in types:
        if not people_organized[type.display_text]:
            people_organized.pop(type.display_text, None)
    return people_organized

@cache_page(60)
def personal(request, name):
    template = loader.get_template('lab/personal.html')
    try:
        person_object = People.objects.filter(url=name)[0]
    except:
        raise Http404
    short_names = ShortNames.objects.filter(profile=person_object)
    publications = ShortNamePublicationMapping.objects.filter(short_name__in=short_names).values_list('paper', flat=True).distinct()
    publications_organized = {}
    for publication in publications:
        try:
            publication = Publication.objects.get(pk=publication)
            if publication.disabled == True:
                raise PublicationNotEnabled
        except:
            continue
        if publication.conf_type.name not in publications_organized:
            publications_organized[publication.conf_type.name] = []
        publications_organized[publication.conf_type.name].append(publication)
    # Sorting for year wise paper display

    for key in publications_organized:
        publications_organized[key].sort( key=lambda x: (x.published_year, x.id), reverse=True)
    
    context = {
        'PAGE_TITLE': person_object.name,
        'person': person_object,
        'publications_organized': publications_organized
    }
    return HttpResponse(template.render(context, request))

def research(request):
    template = loader.get_template('lab/research.html')
    context = {
        'PAGE_TITLE': 'Research Focus Areas'
    }
    return HttpResponse(template.render(context, request))

def flush(request):
    if request.user.is_superuser:
        cache.clear()
        return HttpResponse('Done! :)')
    return HttpResponse('Why don\'t you try after logging in ?')

def events(request):
    if request.user.is_superuser:
        print "Yes!"
    template = loader.get_template('lab/research.html')
    context = {
        'PAGE_TITLE': 'Research Focus Areas'
    }
    return HttpResponse(template.render(context, request))


@cache_page(60)
def publications(request):
    template = loader.get_template('lab/publication.html')
    publications = Publication.objects.all().filter(disabled=False)
    publications_organized = {}
    for publication in publications:
        if publication.conf_type.name not in publications_organized:
            publications_organized[publication.conf_type.name] = []
        publications_organized[publication.conf_type.name].append(publication)
    # Sorting for year wise paper display
    for key in publications_organized:
        publications_organized[key].sort( key=lambda x: (x.published_year, x.id), reverse=True)
        
    context = {
        'PAGE_TITLE': 'Publications',
        'publications_organized': publications_organized
    }
    return HttpResponse(template.render(context, request))

@cache_page(60)
def archive(request):
    template = loader.get_template('lab/archive.html')
    context = {
        'PAGE_TITLE': 'NEWS Archive',
        'news': News.objects.all()
    }
    return HttpResponse(template.render(context, request))


def contact(request):
    template = loader.get_template('lab/contact.html')
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "New form entry on serc.iiit.ac.in by " + form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + '<br>Contact number: ' + str(form.cleaned_data['phone'])
            try:
                send_mail(subject, message, from_email, ['shivam.khandelwal@research.iiit.ac.in'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    context = {
        'PAGE_TITLE': 'Contact',
        'form': form
    }
    return HttpResponse(template.render(context, request))

def thanks(request):
    return HttpResponse('Thank you for your message.')

