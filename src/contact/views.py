from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings

from .forms import ContactForm
# Create your views here.


def contact_us(request, from_view='posts:list'):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print("instance.to_name:", instance.to_name)
        if instance.to_name == 'EM':
            to_email = 'etam22@gmail.com'
        elif instance.to_name == 'HO':
            to_email = 'hben592@gmail.com'
        to_email = [to_email]
        formatted_message = (
            'You\'ve received mail from {person!s}.'
            '\n\nTheir e-mail is {email!s}'
            ' \n\nTheir message is displayed below \n\n{message!s}').format(
                person=instance.from_name,
                email=instance.from_email,
                message=instance.message)
        try:
            send_mail('You got gimmeth.at mail!', formatted_message,
                      settings.EMAIL_HOST_USER, to_email)
        except:
            instance.email_failed = True
        instance.save()
        messages.success(request, "Message received - thanks!")
        print("about to redirect")
        return redirect(from_view)

    return form
