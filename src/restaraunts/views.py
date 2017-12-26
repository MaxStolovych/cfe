from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

# Create your views here.
#function based view

def home(request):
    return render(request, "home.html", {})

def about(request):
    return render(request, "about.html", {})

def contacts(request):
    return render(request, "contacts.html", {})

class HomeView(TemplateView):
    template_name = 'home.html'
    
    
class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contacts.html'