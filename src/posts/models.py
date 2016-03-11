from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify

# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    image = models.ImageField(null=True, blank=True,
                              upload_to=upload_location,
                              width_field="width_field",
                              height_field="height_field")
    slug = models.SlugField(unique=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to=upload_location,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    category = models.ForeignKey(Category)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-date_added"]


def create_slug(descriptor, new_slug=None):
    slug = slugify(descriptor)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(descriptor, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance.title)

pre_save.connect(pre_save_post_receiver, sender=Post)
