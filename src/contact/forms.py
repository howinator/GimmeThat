from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div

from captcha.fields import ReCaptchaField

from .models import Contact


class ContactForm(forms.ModelForm):
    """ Creates contact form with default bootstrap formatting.

    We're using crispy_forms here to deal with formatting of the form with
    bootstrap. crispy_forms also lets us order the fields and wrap fields
    in Div(s) among other things.
    Honestly, forms are one of the last pieces of 'black magic' left
    in django for me."""

    def __init__(self, *args, **kwargs):
        """ Set up the form with all the fields and HTML information."""
        super(ContactForm, self).__init__(*args, **kwargs)
        # TODO figure out exactly what the FormHelper object is capable of
        self.helper = FormHelper()
        # set a few attributes in the HTML
        self.helper.form_id = 'id_contactForm'
        self.helper.form_method = 'post'
        # form_action will call the specified url. This accepts a URL name
        # which I preface with the namespace.
        # This means when they hit submit, the data will be POST to /contact/
        # which will be handled by that view
        self.helper.form_action = 'contact:contact_us'

        # the layout object is formed from layout objects
        self.helper.layout = Layout(
            # Wrap fields in a Fieldset with a legend of
            # 'Want to get in touch?'
            Fieldset(
                'Want to get in touch?',
                # wrap the following fields in its own Div
                # and give that Div a class of css_class
                # I guess the names of the fields need to be the same
                # name as the fields in the model. - not sure
                Div(
                    'from_name',
                    'from_email',
                    'to_name',
                    'message',
                    'captcha',
                    css_class='form-text-fields'
                )))

        # change label on fields. You can change the label of a field
        # at the model level or the form label. verbose_name is how you would
        # change it at the form level. I went with the form level because
        # I don't know where else it might be used
        self.fields['from_name'].label = "Your Name"
        self.fields['from_email'].label = "Your E-mail"
        self.fields['to_name'].label = "Who would you like to contact?"
        self.fields['message'].label = "Your message"

        self.helper.add_input(Submit('submit', 'Submit'))

    # Since this is a model field, we need to tell django which fields
    # from the model will be used
    class Meta:
        model = Contact
        fields = [
            "from_name",
            "from_email",
            "to_name",
            "message",

        ]
    # use radio buttons for who to contact and use the choices
    # in the model. DRY AF
    CONTACT_WHO_CHOICES = Contact.CONTACT_WHO_CHOICES
    to_name = forms.ChoiceField(choices=CONTACT_WHO_CHOICES,
                                widget=forms.RadioSelect)
    # since captcha isn't a field in the model, we need to
    # add it directly to the form
    captcha = ReCaptchaField()
