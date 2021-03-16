from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django_resized import ResizedImageField
import datetime
import os, time

def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'profile/PIC-%s.%s' % (instance.get_created(), extension)

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_pic = ResizedImageField(size=[500, 500],default="profile/avatar.svg",upload_to=upload_location,blank=False,) 
    bio = models.TextField(max_length=200,blank=True, null=True)
    country = CountryField(default='IN')
    facebook_url = models.URLField(blank=True,null=True)
    instagram_url = models.URLField(blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True,auto_now=False, auto_now_add=False, default=datetime.date(1997,10,19) )
    
    class Meta:
        verbose_name ="Profile api"
        verbose_name_plural = "Profiles api"

    def get_absolute_url(self):
        return reverse("profile:profile-detail", kwargs={"username": self.user.username})
    
    def get_created(self):
        dt_obj = time.strftime("%Y%d%m%I%M%S")
        return dt_obj

    def __str__(self):
        return str(self.user)
        
    def all_post(self):
        return self.posts.all().count()

    def __unicode__(self):
        return str(self.user)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)