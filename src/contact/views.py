from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings

from .forms import ContactForm
# Create your views here.


def contact_us(request):
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
        send_mail('You got gimmeth.at mail!', formatted_message,
                  settings.EMAIL_HOST_USER, to_email)
        instance.save()
        messages.success(request, "Message sent! Thank you.")
        print("about to redirect")
        return redirect("posts:list")
    context = {
        "contact_form": form
    }

    return render(request, "contact/contact_us.html", context)

