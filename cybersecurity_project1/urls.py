from .app.views import homePageView, addPostView, deletePostView, displayAttachmentView, signupView, profileView, followProfileView
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

"""cybersecurity_project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


urlpatterns = [
    path(
        'accounts/login/',
        LoginView.as_view(template_name='login.html'),
        name='login'
    ),
   	path(
        'accounts/logout/',
        LogoutView.as_view(next_page='/'),
        name="logout"
    ),
   	path(
        'accounts/signup/',
        signupView,
        name="signup"
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        homePageView,
        name='home'
    ),
    path(
        'profile/<int:profileid>/',
        profileView,
        name='profile'
    ),
    path(
        'profile/<int:profileid>/follow',
        followProfileView,
        name='profile-follow'
    ),
    path(
        'profile/<int:profileid>/posts/add/',
        addPostView,
        name='add-post'
    ),
    path(
        'profile/<int:profileid>/posts/<int:postid>/attachment/<int:attachmentid>',
        displayAttachmentView,
        name='post-attachment-show'
    ),
    path(
        'profile/<int:profileid>/posts/<int:postid>',
        deletePostView,
        name='delete-post'
    ),
]
