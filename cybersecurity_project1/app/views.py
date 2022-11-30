from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import PostAttachment, Post, Profile
from .forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt # A01:2021 – Broken Access Control
def deletePostView(request, profileid, postid):
    post_instance = Post.objects.get(pk=postid)
    profileid = post_instance.profile.id
    post_instance.delete() if post_instance.profile.user == request.user else HttpResponseForbidden()
    return redirect('profile', profileid=profileid)


@login_required
def displayAttachmentView(request, profileid, postid, attachmentid):
    f = PostAttachment.objects.get(pk=attachmentid)
    try:
        response = HttpResponse(f.content, content_type=f.content_type)
        return response # if f.profile.user == request.user or f.user.profile in request.user.profile.following else HttpResponseForbidden()
    except ValueError:
        return HttpResponseNotFound()


@login_required
def addPostView(request, profileid):
    if request.method == 'POST':
        new_post_form = PostForm(data=request.POST, files=request.FILES, )
        if new_post_form.is_valid():
            post = Post(
                profile=request.user.profile,
                content=request.POST.get('content'),
                public=not not request.POST.get('public'),
                upload_date = datetime.now()
            )
            post.save()
            for attachment in request.FILES.getlist('attachment'):
                file = PostAttachment(
                    post=post,
                    content=attachment,
                    content_type = attachment.content_type
                )
                file.save() # A04:2021-Insecure design (users are allowed to upload arbitary files)
            return redirect('profile', profileid=profileid)
        else:
            pass
    else:  
        new_post_form = PostForm()
    return render(request, "new_post.html", {'new_post_form': new_post_form})

@login_required
def followProfileView(request, profileid):
    profile = request.user.profile
    profile.following.add(profileid)
    profile.save()
    return redirect('profile', profileid=profileid)

@login_required
def homePageView(request):
    posts = Post.objects.filter(
        profile__in=Profile.objects.filter(
            id__in=Profile.objects.get(user=request.user).following.values('id')
        )
    )
    suggested_profiles = Profile.objects.filter(~Q(id=request.user.profile.id))
    return render(
        request,
        'home.html',
        {
            'posts': posts,
            'is_follower': True,
            'is_own_profile': False,
            'suggested_profiles': suggested_profiles
        }
    )

def profileView(request, profileid):
    profile = Profile.objects.get(id=profileid)
    suggested_profiles = Profile.objects.filter(
        ~Q(id=request.user.profile.id)
    ) if request.user.is_authenticated else Profile.objects.all()
    return render(
        request,
        'profile.html',
        {
           'profile': profile,
           'is_follower': profile in request.user.profile.following.all() if request.user.is_authenticated else False,
           'is_own_profile': profileid == request.user.profile.id if request.user.is_authenticated else False,
           'posts': Post.objects.filter(profile=profile),
           'suggested_profiles': suggested_profiles
        }
    )

def signupView(request):
    user_form = UserCreationForm(request.POST, request.FILES)
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            login(
                request,
                authenticate(
                    username=user_form.cleaned_data.get('username'),
                    password=user_form.cleaned_data.get('password1')
                )
            )
            redirect('/')
    return render(request, 'signup.html', {'form': user_form})

def searchPostsView(request):
    query_string = request.GET.get('q')
    posts = Post.objects.raw(
        "SELECT * FROM app_post WHERE content LIKE '%%%s%%'" % query_string)  # A03-2021 Injection
    # posts = Post.objects.filter(content__contains=query_string)
    return render(request, 'search.html', {'posts': posts, 'query_string': query_string})
    
