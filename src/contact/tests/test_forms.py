from django.test import TestCase

from .forms import ContactForm


class ContactFormTest(TestCase):

    def test_valid_data(self):
        from_name = 'AT test from_name'
        from_email = 'test@gimmeth.at'
        to_name = 'HO'
        message = 'This is an automated test from test_valid_data'

        form = ContactForm({
            'from_name': from_name,
            'from_email': from_email,
            'to_name': to_name,
            'message': message
        })

        self.assertTrue(form.is_valid())
        saved_comment = form.save()
        self.assertEqual(saved_comment.from_name, from_name)
        self.assertEqual(saved_comment.from_email, from_email)
        self.assertEqual(saved_comment.to_name, to_name)
        self.assertEqual(saved_comment.message, message)

