""" Tests the e-mail and model saving functionality in contact. """

import contact.views
from contact.models import Contact
from contact.tests.test_forms import ContactFormTest

from django.http import HttpRequest
from django.test import TestCase
from django.core import mail
from django.contrib import messages

from smtplib import SMTPConnectError, SMTPAuthenticationError

from unittest.mock import Mock


class ContactUsViewTest(TestCase):
    """ Tests the ContactUsViewTest.

    This test is composed from the ContactUsFormTest, so that we can use its
    instance variables. This is done in SetUp which is run before each test.
    Since SetUp is run before each test, it shouldn't cause any side effects.
    If I wanted to completely avoid side effects, I'd have to violate DRY.
    In the future, I'll consider violating DRY since side effects are the bane
    of tests.

    """

    def setUp(self):
        """ SetUp is run before each test is run."""

        # I need to instantiate an instance of ContactFormInstance to access
        # the valid form.
        self.formtest = ContactFormTest()
        # Call formtest's SetUp function to set environment variable
        self.formtest.setUp()
        self.formtest.valid_dict['message'] = 'view test'

    def test_failed_email(self):
        """ This tests that failed emails are handled properly in the view.

        We accomplish this by mocking send_mail with an exception.
        We then call contact_us. We then make sure that a record exists
        where failed_email is True. We repeat this procedure for each
        exception in a list."""

        # TODO this test is probably too long. I wrote it like this because
        # it's qucik and easy to change which exceptions we're checking for.
        # Once I have more time I should probably split each exception
        # into a new test.

        # Create mock send_mail which will raise an SMTPConnectionError inside
        # the contact_us view when the view is called.
        messages.success = Mock(return_value=None)
        # Set up the request object with all the requisite fields
        request = HttpRequest()
        request.method = 'POST'
        # I need to append the valid form data to the request.POST dict-like
        # object
        # Just FYI all the form fields are just key-value pairs in the
        # request.POST dictionary-like object. These pairs are unpacked into
        # the form. Until then, fields are just keys and values
        request.POST.update(self.formtest.valid_dict)

        # There shouln't be any contact records yet
        failed_contacts = Contact.objects.filter(email_failed__exact=True)
        # If the query set is truly empty, it will evaluate to False
        self.assertFalse(failed_contacts)

        # create list of common exceptions from send_mail
        possible_exceptions = [
            SMTPAuthenticationError(2, 'Authentication Error'),
            SMTPConnectError(2, 'Connection error'),
            TypeError('Type Error')
        ]
        # Initialize a count of contacts before we start raising exceptions
        count_contacts = Contact.objects.filter(email_failed__exact=True)
        count_contacts = count_contacts.count()

        # loop through the exceptions and mock send_mail for each
        for excep in possible_exceptions:
            mail.send_mail = Mock(side_effect=excep)
            # call the view to see how it handles the exception
            contact.views.contact_us(request)
            # Find any contact records where email_failed is True.
            # If the view handled the exception correctly, that means there is
            # one more contact object where email_failed is True than
            # from the previous iteration
            failed_contacts_list = Contact.objects.filter(
                email_failed__exact=True
            )
            self.assertEqual(failed_contacts_list.count(), count_contacts + 1)
            # Update the count of failed contacts and move on to the next
            # exception
            count_contacts = failed_contacts_list.count()

    def tearDown(self):
        """ tearDown the Contact View Test. """

        # Need to tear down the form object
        self.formtest.tearDown()
