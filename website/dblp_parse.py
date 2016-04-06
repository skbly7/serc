### CONFIGURE HERE
dblp_url = "http://dblp.uni-trier.de/pers/xx/k/Kulkarni:Naveen_N=.xml"
###

import urllib
import xmltodict
from django.db import IntegrityError
from lab.models import *

f = urllib.urlopen(dblp_url)
data = f.read()
arr = xmltodict.parse(data)
try:
    all_publication = arr['dblpperson']['r']
except:
    all_publication = None

print "--------------------- FETCH SUCCESSFUL -----------------------"
count = 1
for publication in all_publication:
    print '------------------------------ ENTRY #'+ str(count) +' ---------------------------------'
    type = publication.keys()[0]
    if type == "article":
        other_info = publication[type]
        type = 1
        year = other_info['@mdate'].split('-')[0]
        if isinstance(other_info['author'], list):
            authors_comma_separated = ', '.join(other_info['author'])
        else:
            authors_comma_separated = other_info['author']
        title = other_info['title']
        try:
            published_at = other_info['journal']
        except:
            published_at = other_info['booktitle']
        try:
            page = other_info['pages']
        except:
            page = ''
    if type == "inproceedings":
        other_info = publication[type]
        type = 2
        year = other_info['@mdate'].split('-')[0]
        if isinstance(other_info['author'], list):
            authors_comma_separated = ', '.join(other_info['author'])
        else:
            authors_comma_separated = other_info['author']
        title = other_info['title']
        published_at = other_info['booktitle']
        try:
            page = other_info['pages']
        except:
            page = ''
    if type == "proceedings":
        other_info = publication[type]
        type = 4
        year = other_info['@mdate'].split('-')[0]
        if isinstance(other_info['editor'], list):
            authors_comma_separated = ', '.join(other_info['editor'])
        else:
            authors_comma_separated = other_info['editor']
        title = other_info['title']
        try:
            published_at = other_info['series']['#text']
        except:
            published_at = other_info['publisher']
        try:
            page = other_info['volume']
        except:
            page = ''
    try:
        url = other_info['ee']
    except:
        url = 'http://dblp.uni-trier.de/' + other_info['url']
    if isinstance(url, list):
        url = url[0]
    type = ConferenceType.objects.get(id=type)
    entry = {'conf_type': type, 'published_year': year, 'authors_comma_separated': authors_comma_separated, 'title': title, 'published_at': published_at, 'link': url, 'published_page': page}
    try:
        entry = Publication(conf_type=type, published_year=year, authors_comma_separated=authors_comma_separated, title=title, published_at=published_at, link=url, published_page=page)
        count += 1
        print entry.title
        entry.save()
    except IntegrityError:
        print "ALREADY EXIST: " + title


