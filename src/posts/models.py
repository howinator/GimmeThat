from django.db import models

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length = 250)
	content = models.TextField()
	last_modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	date_added = models.DateTimeField(auto_now = False, auto_now_add = True)


	def __str__(self):
		return self.title