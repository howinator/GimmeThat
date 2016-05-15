from contact.forms import ContactForm
from contact.models import Contact
from django.test import TestCase


import os


class ContactFormTest(TestCase):
    """ Tests the contact form.

    Instance variables:

    val_from_name -- valid from name
    val_from_email -- valid email address
    val_to_name -- valid choice for who it's going to
    val_message -- valid message
    valid_form -- a valid form

    """

    def setUp(self):
        """Set up contact test."""

        # Set environment variable so that we can get around recaptcha
        os.environ['RECAPTCHA_TESTING'] = 'True'

        # Make a bunch of valid fields for the valid form
        self.val_from_name = 'AT test val_from_name'
        self.val_from_email = 'test@gimmeth.at'
        self.val_to_name = 'HO'
        self.val_message = 'This is an automated test from test_valid_data'
        # Make a dictionary of all the valid fields which can be used later
        self.valid_dict = {
            'from_name': self.val_from_name,
            'from_email': self.val_from_email,
            'to_name': self.val_to_name,
            'message': self.val_message,
            'g-recaptcha-response': 'PASSED'
        }

        # Create the valid form
        self.valid_form = ContactForm(self.valid_dict)

    def test_valid_data_equals_valid_form(self):
        """ Tests that form is valid. """

        self.assertTrue(self.valid_form.is_valid())

    def test_data_goes_into_object(self):
        """ Tests all fields go into object model correctly. """

        saved_comment = self.valid_form.save()
        self.assertEqual(saved_comment.from_name, self.val_from_name)
        self.assertEqual(saved_comment.from_email, self.val_from_email)
        self.assertEqual(saved_comment.to_name, self.val_to_name)
        self.assertEqual(saved_comment.message, self.val_message)

        # TODO: This probable belongs ina model test.
        contact_queryset = Contact.objects.filter(
            message__exact=self.val_message)
        first_object = contact_queryset[0]
        self.assertEqual(first_object.from_name, self.val_from_name)

    def tearDown(self):
        """ Unset everything that needs to be unset before next test. """

        os.environ['RECAPTCHA_TESTING'] = 'False'
