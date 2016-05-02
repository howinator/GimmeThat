from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Contact


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_contactForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Contact
        fields = [
            "to_name",
            "message",
            "from_name",
            "from_email",
        ]
