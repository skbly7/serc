from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_str

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


class SiteTextData(models.Model):
    unique_identifier = models.CharField(max_length=20)
    data = models.TextField()

    def __str__(self):
        return self.unique_identifier


DISP_CHOICE = ((4, '4 in a row'), (6, '6 in a row'))

class PeopleType(models.Model):
    name = models.CharField(max_length=40)
    display_text = models.CharField(max_length=40)
    show_research_interest = models.BooleanField(default=False)
    count_in_one_row = models.IntegerField(choices=DISP_CHOICE, default=2)
    order = models.IntegerField(default=6)
    def __str__(self):
        return self.name

class People(models.Model):
    list_on = models.ForeignKey(PeopleType)
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=100, blank=True)
    interest = models.TextField(blank=True)
    url = models.CharField(max_length=20, blank=True)
    personal_page = models.BooleanField(default=False)
    short_bio = models.TextField(blank=True)
    study_one_line = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    homepage = models.CharField(max_length=100, blank=True)
    login = models.OneToOneField(User, blank=True, null=True)
    img = models.ImageField(upload_to='static/images/people')
    display_priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def http_link(self):
        return '/personal/' + self.url


class ShortNames(models.Model):
    name = models.CharField(max_length=30)
    profile = models.ForeignKey(People, blank=True, null=True)

    def __str__(self):
        return (self.name).encode('ascii', 'ignore')

    def display(self):
        if self.profile is None:
            return self.__str__()
        else:
            return '<a href="/personal/' + self.profile.url + '">' + self.__str__() + '</a>'

class ConferenceType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Publication(models.Model):
    authors_comma_separated = models.CharField(default='', max_length=500)
    conf_type = models.ForeignKey(ConferenceType)
    published_at = models.CharField(max_length=200)
    published_page = models.CharField(max_length=20, blank=True)
    published_year = models.IntegerField()
    title = models.CharField(max_length=200, unique=True)
    link = models.URLField(blank=True)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return smart_str(self.title)

    def authors(self):
        list = []
        all_authors = self.authors_comma_separated.split(',')
        for author in all_authors:
            author = ShortNames.objects.get(name=author.strip())
            list.append(author.display())
        return ', '.join(list)

    def save(self, *args, **kwargs):
        super(Publication, self).save(*args, **kwargs)
        all_authors = self.authors_comma_separated.split(',')
        ShortNamePublicationMapping.objects.filter(paper=self).delete()
        for author in all_authors:
            author = author.strip()
            if author == "":
                continue
            short_name, created = ShortNames.objects.get_or_create(name=author)
            mapping = ShortNamePublicationMapping(short_name=short_name, paper=self)
            mapping.save()


class ShortNamePublicationMapping(models.Model):
    short_name = models.ForeignKey(ShortNames)
    paper = models.ForeignKey(Publication)

    def __str__(self):
        return str(self.short_name) + str(self.paper)

class SocialIcon(models.Model):
    name = models.CharField(max_length=20)
    link = models.URLField()
    icon = models.ImageField(upload_to='static/images/social')

    def __str__(self):
        return (self.name).encode('ascii', 'ignore')

    def view(self):
        return '<a href="' + self.link + '" target="_blank" alt="' + self.name + '"><img src="/' + str(self.icon) + '" /></a>'

DISP_CHOICE = ((1, 'Type = Link'), (2, 'Type = Project'), (3, 'Type = Courses'), (4, 'Type = Under construction'))

class ResourceType(models.Model):
    name = models.CharField(max_length=40)
    url_path = models.CharField(max_length=10, unique=True)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.name

