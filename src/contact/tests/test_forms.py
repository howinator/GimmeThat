from contact.forms import ContactForm
from contact.models import Contact
from django.test import TestCase


import os


class ContactFormTest(TestCase):

    def setUp(self):
        """Set up contact test."""

        os.environ['RECAPTCHA_TESTING'] = 'True'

        self.from_name = 'AT test from_name'
        self.from_email = 'test@gimmeth.at'
        self.to_name = 'HO'
        self.message = 'This is an automated test from test_valid_data'

        self.valid_form = ContactForm({
            'from_name': self.from_name,
            'from_email': self.from_email,
            'to_name': self.to_name,
            'message': self.message,
            'g-recaptcha-response': 'PASSED'
        })

    def test_valid_data(self):
        """ Tests correct things happen with valid data. """

        print("running test_valid_data")

        self.assertTrue(self.valid_form.is_valid())
        saved_comment = self.valid_form.save()
        self.assertEqual(saved_comment.from_name, self.from_name)
        self.assertEqual(saved_comment.from_email, self.from_email)
        self.assertEqual(saved_comment.to_name, self.to_name)
        self.assertEqual(saved_comment.message, self.message)

        contact_queryset = Contact.objects.filter(message__exact=self.message)
        first_object = contact_queryset[0]
        self.assertEqual(first_object.from_name, self.from_name)

    def tearDown(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'
