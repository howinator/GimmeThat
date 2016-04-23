from django.test import TestCase
from django.core.mail import send_mail

class EmailTestCase(TestCase):
    def test_email_sends(self):
        response_from_matches = send_mail('Test | from matches', 
            'This test is where from_email matches host_email', 
            'howie@gimmeth.at', ['hben592@gmail.com'])
        response_from_not_match = send_mail('Test | from does not match',
            'This test is where from_email does not match host_email',
            'howiethebot@gmail.com', ['hben592@gmail'])
        print(response_from_not_match)
        self.assertEqual(response_from_matches, 1)
        self.assertEqual(response_from_not_match, 1)
