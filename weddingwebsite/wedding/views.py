from django.shortcuts import render
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'home.html', context={
        'contact_info': settings.CONTACT_INFO,
    })