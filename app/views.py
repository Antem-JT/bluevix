from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import PostForm, MyUserCreationForm, UserForm, VideoForm
from .models import Post, User, Comment, Video, VideoComment
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            messages.error(request, 'Password Incorrect')
        except:
            messages.error(request, 'User Does not Exist')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def registerUser(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(location__icontains =q) |
        Q(hashtag__icontains =q) |
        Q(user__name__icontains =q) |
        Q(description__icontains =q) |
        Q(user__username__icontains =q) 
    )
    comments = Comment.objects.filter()[0:2]
    # post = get_object_or_404(Post)
    # if request.user in post.likes.all():
    #     post.likes.remove(request.user)
    # else:
        # post.likes.add(request.user)

    # post = get_object_or_404(Post, id=posts)
    # if request.user.is_authenticated:
    #     if request.method == "POST":
    #         post.likes.add(request.user)
    #     else:
    #         post.likes.remove(request.user)

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('home')

    context = {'posts':posts, 'comments':comments}
    return render(request, 'home.html', context)


def videos(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    videos = Video.objects.filter(
        Q(hashtag__icontains =q) |
        Q(user__name__icontains =q) |
        Q(description__icontains =q) |
        Q(user__username__icontains =q) 
    )
    comments = VideoComment.objects.filter()[0:2]
    context = {'videos': videos, 'comments':comments}
    return render(request, 'videos.html', context)


def add_comment(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        text = request.POST.get('text')
        comment = Comment.objects.create(
            post_id = post_id,
            user = request.user,
            text = text,
        )
        comment.save()
        return redirect('home')
    return redirect('home')


def add_comment_video(request):
    if request.method == "POST":
        video_id = request.POST.get('video_id')
        text = request.POST.get('text')
        comment = VideoComment.objects.create(
            video_id = video_id,
            user = request.user,
            text = text,
        )
        comment.save()
        return redirect('reals')
    return redirect('reals')


def like(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        new_like_count = post.likes.count()
        return JsonResponse({'new_like_count': new_like_count})

    return redirect('home')


def videolike(request):
    if request.method == "POST":
        video_id = request.POST.get('video_id')
        video = Video.objects.get(pk=video_id)
        if request.user in video.likes.all():
            video.likes.remove(request.user)
            liked = False
        else:
            video.likes.add(request.user)
            liked = True
        
        new_like_count = video.likes.count()
        return JsonResponse({'new_like_count': new_like_count})
    return redirect('reals')


# def likes(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     # if request.method == "POST":
#     if request.user in post.likes.all():
#         post.likes.add(request.user)
#     else:
#         post.likes.add(request.user)
    
#     # else:
#     #     post.likes.remove(request.user)

#     return redirect('home')


def postForm(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
        # post = Post.objects.get_or_create(
        #     user = request.user,
        #     image = request.FILES.get('image'),
        #     description = request.POST.get('description')
        # )
    context = {'form': form}
    return render(request, 'post.html', context)


def videoForm(request):
    form = VideoForm()
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('reals')
        # post = Post.objects.get_or_create(
        #     user = request.user,
        #     image = request.FILES.get('image'),
        #     description = request.POST.get('description')
        # )
    context = {'form': form}
    return render(request, 'video.html', context)


def profleUser(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    # if request.method == "POST":
    #     user.followers.add(request.user)
    # elif request.method == "POST":
    #     user.followers.remove(request.user)
    # if request.method == "POST":
    #     user_to_follow = User.objects.get(id=pk)
    #     follow_object, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    #     follow_object.save()
    #     return redirect('profile', pk=user.id)

    context = {'user': user, 'posts':posts}
    return render(request, 'profile.html', context)


def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    context = {'form': form}
    return render(request, 'edit_profile.html', context)


def editPost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'edit-post.html', context)

def editvideo(request, pk):
    video = Video.objects.get(id=pk)
    form = VideoForm(instance=video)
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('reals')
    context = {'form': form}
    return render(request, 'edit-video.html', context)

def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.delete()    
        return redirect('home')
    context = {'post': post}
    return render(request, 'delete-post.html', context)


def deleteVideo(request, pk):
    video = Video.objects.get(id=pk)
    if request.method == "POST":
        video.delete()    
        return redirect('reals')
    context = {'video': video}
    return render(request, 'delete-video.html', context)


def peoplesUsers(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    users = User.objects.filter(
        Q(username__icontains=q) |
        Q(name__icontains =q)
    )
    context = {'users':users}
    return render(request, 'peoples.html', context)

def follow(request, pk):
    user = User.objects.get(id=pk)
    user.followers.add(request.user)
    return redirect('profile', pk=user.id)

def unfollow(request, pk):
    user = User.objects.get(id=pk)
    user.followers.remove(request.user)
    return redirect('profile', pk=user.id)