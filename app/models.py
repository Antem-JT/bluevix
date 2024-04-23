from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=300, null=True)
    email = models.EmailField(unique=True)
    about = models.TextField(null=True)
    avatar =  models.ImageField(null=True, default='avatar.svg', upload_to='')
    coverpic = models.ImageField(null=True, default='bg.jpg', upload_to='coverPhotos')
    location = models.CharField(max_length=300, null=True, blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    verified = models.BooleanField(default=False)
    


class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images-post/')
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add = True)
    hashtag = models.CharField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=300, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = [ '-updated', '-created' ]

    def __str__(self):
        return self.description



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField(null = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created'][:2]

    def __str__(self):
        return self.text
      


class Video(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    description = models.TextField()
    hashtag = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=300, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='video_likes', blank=True)
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = [ '-updated', '-created' ]

    def __str__(self):
        return self.description
    


class VideoComment(models.Model):
    video = models.ForeignKey(Video, on_delete = models.CASCADE, related_name = "comments")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField(null = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created'][:2]

    def __str__(self):
        return self.text