from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display =["__str__", "date_added"]
	list_display_links = ["date_added", "__str__"]
	list_filter = ["date_added", "last_modified"]
	search_fields = ["title", "content"]
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)