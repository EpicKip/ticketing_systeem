from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.template.response import TemplateResponse
from tickets.models import Event


def index(request):
    events = Event.objects.all()
    return render_to_response('index.html', {'events': events}, context_instance = RequestContext(request))