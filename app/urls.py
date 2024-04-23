from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('post-form/', views.postForm, name='post-form'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('profile/<str:pk>', views.profleUser, name='profile'),
    path('update-user/', views.UpdateUser, name='update-user'),
    path('people/', views.peoplesUsers, name='people'),
    path('edit-post/<str:pk>', views.editPost, name='edit-post'),
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    path('t/<str:pk>', views.follow, name='t'),
    path('a/<str:pk>', views.unfollow, name='a'),
    path('like/', views.like, name='like'),
    path('comment/', views.add_comment, name='comment'),
    path('comments/', views.add_comment_video, name='comments'),
    path('reals/', views.videos, name='reals'),
    path('delete-video/<str:pk>', views.deleteVideo, name='delete-video'),
    path('video-form/', views.videoForm, name='video-form'),
    path('edit-video/<str:pk>', views.editvideo, name='edit-video'),
    path('videolike/', views.videolike, name='videolike'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)