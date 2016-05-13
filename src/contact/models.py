from django.db import models

# Create your models here.


class Contact(models.Model):
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
    email_failed = models.NullBooleanField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
