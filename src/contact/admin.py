from django.contrib import admin

from .models import Contact
# Register your models here.


class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('from_name', 'to_name', 'date_added')

admin.site.register(Contact)
