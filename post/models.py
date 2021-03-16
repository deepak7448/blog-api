from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django_resized import ResizedImageField
from django.shortcuts import reverse
from profiles.models import Profiles
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
import time

def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'post/IMG-%s.%s' % (instance.get_created(), extension)

class post(models.Model):
    author=models.ForeignKey(Profiles, on_delete=models.CASCADE,related_name="posts")
    # title= models.CharField(max_length=20)
    # slug = AutoSlugField(populate_from='title',
    #                       unique_with=['title',],
    #                       slugify=custom_slugify,
    #                       always_update=True)
    content = models.TextField(max_length=10000,blank=True, null=True)
    image = ResizedImageField(size=[800, 800],upload_to=upload_location,blank=True, null=True)
    liked = models.ManyToManyField(User,blank=True,related_name="likes")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name ="Post api"
        verbose_name_plural ="Posts api"

    # def get_user_url(self):
    #     return reverse("profile:profile-detail", kwargs={"author": self.author.user})
    
    def get_absolute_url(self):
        return reverse("posts:post-details", kwargs={"pk": self.pk})

    def get_like_url(self):
        return reverse("posts:post-like", kwargs={"pk": self.pk})
    
    def get_total_likes(self):
        return self.liked.count()

    def get_created(self):
        dt_obj = time.strftime("%Y%d%m%I%M%S")
        return dt_obj

    def images(self):
        if self.image:
            return f"http://{Site.objects.get_current()}/media/" + str(self.image)
        else:
            return None

    def contents(self):
        if self.content:
            return f"{self.content[:100]}..."
        else:
            return None

    def comment_count(self):
        return self.postcomment_set.all().filter(reply=None).count()

    def __str__(self):
        return self.content[:10]

    def __unicode__(self):
        return self.content[:10]


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(reply=None)
        return qs

class Comment(models.Model):
    author=models.ForeignKey(Profiles, on_delete=models.CASCADE,related_name="post_comment")
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    reply = models.ForeignKey("self",blank=True, null=True, on_delete=models.CASCADE,related_name="comment_replies")
    created_on = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()
    
    class Meta:
        verbose_name ="Comment api"
        verbose_name_plural ="Comments api"

    def __str__(self):
        return self.comment

    def replys(self):
        return Comment.objects.filter(reply=self)

    @property
    def is_reply(self):
        if self.reply is not None:
            return True
        return False

    # def get_absolute_url(self):
    #     return reverse("Comment_detail", kwargs={"pk": self.pk})

