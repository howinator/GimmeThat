from django.db import models

# Create your models here.


class Contact(models.Model):
    """ Defines the model that will be saved when a user gets in touch.

    When someone tries to Emily or I, I wanted to save a record of that
    contact in the database. There's a few reasons for this:
        1) I want to be able to look back and who contacted us.
        2) In case we delete an e-mail.
        3) In case an e-mail fails to send.
    """
    # TODO use e-mails and names in user authentication table
    EMILY = 'EM'
    HOWIE = 'HO'
    CONTACT_WHO_CHOICES = (
        (EMILY, 'Emily (the brain)'),
        (HOWIE, 'Howie (the muscle)'),
    )
    message = models.TextField(max_length=5000)
    to_name = models.CharField(max_length=2,
                               choices=CONTACT_WHO_CHOICES)
    from_name = models.CharField(max_length=200)
    from_email = models.EmailField()
    # NullBooleanField is allowed ot be null by default
    email_failed = models.NullBooleanField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
