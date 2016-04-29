from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.


def contact_us(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        
