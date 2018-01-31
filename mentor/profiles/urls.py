"""mentor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from . import views
from django.conf.urls import include, url
from posts import urls as posts_urls

urlpatterns = [
    url(r'^(?P<username>[\w]+)/$', views.UserProfileView.as_view(), name="userprofile"),
    url(r'^(?P<username>[\w]+)/block/$', views.block_user_view, name="block"),
    url(r'^(?P<username>[\w]+)/follow/$', views.make_new_follow_view, name="follow"),
    url(r'^(?P<username>[\w]+)/unblock/$', views.unblock_user_view, name="unblock"),
    url(r'^(?P<username>[\w]+)/unfollow/$', views.delete_follow_view, name="unfollow"),
    # Single-user views
    url(r'^(?P<username>[\w]+)/edit/$', views.UserProfileEditView.as_view(), name="edit"),
    url(r'^(?P<username>[\w]+)/posts/', include(posts_urls)),
]
