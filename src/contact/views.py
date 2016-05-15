from django.core import mail
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings

from .forms import ContactForm


def contact_us(request, from_view='posts:list'):
    """ Handles the processing of the contact form sent from another view.

    Arguments:
    request -- the request from the client
    from_view -- the view this request was sent from. Default is posts:list

    This view an intermediary view which handles a request fed by a
    client-facing view. contact_us does a few things:
    If there is a POST method on the request:
    First, the view receives the request and the view that it was sent from.
    Second, it makes the form from the request.
    Third, it sets up the e-mail and sends the e-mail.
    Fourth, it attaches a success message and redirects to from_view.
    If there isn't an attached POST method, it makes the empty form and
    returns it.
    """

    # need to initialize form with data from POST or blank form
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # create Contact object, but don't save it to the database
        instance = form.save(commit=False)
        # TODO package this into a utility function or class
        # Need to use the key for the choices in the database
        if instance.to_name == 'EM':
            to_email = 'etam22@gmail.com'
        elif instance.to_name == 'HO':
            to_email = 'hben592@gmail.com'
        # to_email needs to be a list
        to_email = [to_email]
        # TODO This should bt the __str__ of the object
        formatted_message = (
            'You\'ve received mail from {person!s}.'
            '\n\nTheir e-mail is {email!s}'
            ' \n\nTheir message is displayed below \n\n{message!s}').format(
                person=instance.from_name,
                email=instance.from_email,
                message=instance.message)
        # the sending of the email mail fail, so we need to flag the e-mail as
        # failed. Failed emails need to be handled at a later time
        try:
            mail.send_mail('You got gimmeth.at mail!', formatted_message,
                           settings.EMAIL_HOST_USER, to_email)
        except:
            instance.email_failed = True

        # Finished handline the instance so we can save and redirect
        instance.save()
        messages.success(request, "Message received - thanks!")
        return redirect(from_view)

    # if form.is_valid() == False return a blank form
    return form
