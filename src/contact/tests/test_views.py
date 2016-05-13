""" Tests the e-mail and model saving functionality in contact. """

import contact.views

from django.test import TestCase, Mock
from django.core.mail import send_mail

from contact.models import Contact
from contact.tests.test_forms import ContactFormTest


from smtplib import SMTPConnectError, SMTPAuthenticationError


class ContactUsViewTest(TestCase):
    """ Tests the ContactUsViewTest.

    This test is composed from the ContactUsFormTest, so that we can use its
    instance variables. This is done in SetUp which is run before each test.
    Since SetUp is run before each test, it shouldn't cause any side effects.
    If I wanted to completely avoid side effects, I'd have to violate DRY.
    In the future, I'll consider violating DRY since side effects are the bane
    of tests.

    """

    def SetUp(self):
        """ SetUp is run before each test is run."""

        # I need to instantiate an instance of ContactFormInstance to access
        # the valid form.
        self.formtest = ContactFormTest()
        # Call formtest's SetUp function to set environment variable
        self.formtest.SetUp()
        self.valid_form = self.formtest.valid_form

    def test_failed_email(self):
        """ This tests that failed emails are handled properly in the view.

        We accomplish this by mocking send_mail with a couple different
        exceptions. We then check to make sure that the exception is
        caught and the failed_email field is set to True."""

        # Create mock send_mail which will raise an SMTPConnectionError inside
        # the contact_us view when the view is called.
        # Below is what I'm replicating
        # >>> from django.core.mail import send_mail
        # >>> from unittest.mock import Mock
        # >>> def try_to():
        # ...   return send_mail('whatever')
        # ...
        # >>> send_mail = Mock(return_value=4)
        # >>> try_to()
        # 4
        # >>> send_mail = Mock(side_effect=Exception('Boom!'))
        # >>> try_to()
        # Traceback (most recent call last):
        # File "<console>", line 1, in <module>
        # File "<console>", line 2, in try_to
        # File "/usr/lib/python3.4/unittest/mock.py", line 896, in __call__
        # return _mock_self._mock_call(*args, **kwargs)
        # File "/usr/lib/python3.4/unittest/mock.py", line 952, in _mock_call
        # raise effect
        # Exception: Boom!

        # I'm pretty sure the below will also work.
        # >>> from unittest import mock
        # >>> def try_to():
        # ...   return send_mail('stuff')
        # ...
        # >>> send_mail = mock.Mock(return_value=4)
        # >>> try_to()
        # 4
        # >>> send_mail = mock.Mock(side_effect=TypeError('bad!'))
        # >>> try_to()
        # Traceback (most recent call last):
        # File "<console>", line 1, in <module>
        # File "<console>", line 2, in try_to
        # File "/usr/lib/python3.4/unittest/mock.py", line 896, in __call__
        # return _mock_self._mock_call(*args, **kwargs)
        # File "/usr/lib/python3.4/unittest/mock.py", line 952, in _mock_call
        # raise effect
        # TypeError: bad!

        send_mail = Mock(side_effect=SMTPConnectError(2, "Connection Error"))
