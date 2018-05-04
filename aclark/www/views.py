from .forms import ContactForm
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
import os
import random
import requests

# Create your views here.

BASE_URL = 'https://%s' % os.environ.get('API_HOST', 'aclark.net')
CLIENT_URL = '%s/api/clients/?format=json' % BASE_URL
SERVICE_URL = '%s/api/services/?format=json' % BASE_URL
TESTIMONIAL_URL = '%s/api/testimonials/?format=json' % BASE_URL
PROFILE_URL = '%s/api/profiles/?format=json' % BASE_URL


def about(request):
    context = {}
    testimonials = requests.get(TESTIMONIAL_URL).json()
    context['testimonial'] = random.choice(testimonials)
    return render(request, 'about.html', context)


def page(request, slug=None):
    context = {}
    return render(request, 'page.html', context)


def blog(request):
    return HttpResponseRedirect('http://blog.aclark.net')


def clients(request):
    context = {}
    clients = requests.get(CLIENT_URL).json()
    context['clients'] = clients
    testimonials = requests.get(TESTIMONIAL_URL).json()
    context['testimonial'] = random.choice(testimonials)
    return render(request, 'clients.html', context)


def contact(request):
    context = {}
    now = timezone.datetime.now
    msg = 'Message sent!'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            message = '\n'.join([message, sender])
            recipients = [settings.EMAIL_FROM]
            subject = settings.EMAIL_SUBJECT % now().strftime(
                '%m/%d/%Y %H:%M:%S')
            send_mail(subject, message, settings.EMAIL_FROM, recipients)
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ContactForm()
    context['form'] = form
    return render(request, 'contact.html', context)


def home(request):
    context = {}
    return render(request, 'page.html', context)


def services(request):
    context = {}
    services = requests.get(SERVICE_URL).json()
    context['services'] = services
    return render(request, 'services.html', context)


def testimonials(request):
    context = {}
    testimonials = requests.get(TESTIMONIAL_URL).json()
    context['testimonials'] = testimonials
    return render(request, 'testimonials.html', context)


def team(request):
    context = {}
    profiles = requests.get(PROFILE_URL).json()
    context['profiles'] = profiles
    return render(request, 'team.html', context)
