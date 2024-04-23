from django.contrib import admin
from .models import User, Post, Comment, Video, VideoComment

# Register your models here.

admins = [User, Post, Comment, Video, VideoComment]
admin.site.register(admins)