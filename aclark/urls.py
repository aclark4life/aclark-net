"""aclarknet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from aclark.db import urls as db_urls
from aclark.db import views as db_views
from aclark.www import views as www_views
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'clients', db_views.ClientViewSet)
router.register(r'services', db_views.ServiceViewSet)
router.register(r'testimonials', db_views.TestimonialViewSet)
router.register(r'profiles', db_views.ProfileViewSet)

urlpatterns = [
    url(r'^$', www_views.home, name='home'),
    url(r'^about$', www_views.about, name='about'),
    url(r'^admin', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^db/', include(db_urls)),
    url(r'^blog$', www_views.blog, name='blog'),
    url(r'^clients$', www_views.clients, name='clients'),
    url(r'^contact$', www_views.contact, name='contact'),
    url(r'^services$', www_views.services, name='services'),
    url(r'^team$', www_views.team, name='team'),
    url(r'^testimonials$', www_views.testimonials, name='testimonials'),
]
