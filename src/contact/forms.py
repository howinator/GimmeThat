from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout

from captcha.fields import ReCaptchaField

from .models import Contact


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_contactForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'contact:contact_us'

        # change label on fields. You can change the label of a field
        # at the model level or the form label. verbose_name is how you would
        # change it at the form level. I went with the form level because
        # I don't know where else it might be used
        self.fields['from_name'].label = "Your Name"
        self.fields['from_email'].label = "Your E-mail"
        self.fields['to_name'].label = "Who would you like to contact?"
        self.fields['message'].label = "Your message"

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Contact
        fields = [
            "from_name",
            "from_email",
            "to_name",
            "message",

        ]
    CONTACT_WHO_CHOICES = Contact.CONTACT_WHO_CHOICES
    to_name = forms.ChoiceField(choices=CONTACT_WHO_CHOICES,
                               widget=forms.RadioSelect)
    captcha = ReCaptchaField()
