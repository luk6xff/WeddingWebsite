from django.shortcuts import render
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse
# Create your views here.

def main_page(request):
    template = get_template('main_page.html')
    variables = {
        'head_title': 'Stay tuned :)',
        'page_title': 'Our wedding site will be available from 15.06.2018 :)',
        'page_body': '                                        Justyna&Lukasz'
    }
    output = template.render(variables)
    return HttpResponse(output)
