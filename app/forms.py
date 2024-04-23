from django.forms import ModelForm
from .models import User, Post, Video
from django.contrib.auth.forms import UserCreationForm

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description', 'hashtag', 'location']

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['video_file', 'description', 'hashtag', 'location']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['coverpic', 'avatar', 'name', 'username', 'email', 'about']