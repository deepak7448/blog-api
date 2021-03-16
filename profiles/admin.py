from django.contrib import admin
from .models import Profiles

# Register your models here.

class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('user','country','facebook_url','instagram_url','date_of_birth')


admin.site.register(Profiles,ProfilesAdmin)
