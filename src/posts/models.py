from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True,
                              upload_to=upload_location,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-date_added"]
