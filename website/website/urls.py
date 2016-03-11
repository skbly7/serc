"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
handler404 = 'lab.views.custom_404'

urlpatterns = [
    url(r'^api/', include('lab.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'lab.views.index', name='index'),
    url(r'^about/$', 'lab.views.about', name='about'),
    url(r'^services/$', 'lab.views.service', name='services'),
    url(r'^research/$', 'lab.views.research', name='research'),
    url(r'^contact/$', 'lab.views.contact', name='contact'),
    url(r'^people/(?P<type>[a-z]+)/$', 'lab.views.people', name='people'),
    url(r'^personal/(?P<name>[a-z.]+)/$', 'lab.views.personal', name='personal'),
    url(r'^logout/$', 'django_cas.views.logout', name='logout'),
    url(r'^login/$', 'django_cas.views.login', name='login'),
    url(r'^archive/$', 'lab.views.archive', name='archive'),
]