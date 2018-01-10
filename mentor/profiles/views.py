from . import models
from braces.views import (LoginRequiredMixin, UserPassesTestMixin)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView

# Class-Based-Views.


class HomeIndexView(TemplateView):
    template_name = "profiles/index.html"


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("index")


class UserProfileEditView(LoginRequiredMixin, UpdateView):

    model = models.UserProfile
    slug_field = 'user__username'
    slug_url_kwarg = "username"
    fields = ['avatar', 'bio']
    template_name = "profiles/profile_update.html"

    def get_success_url(self):
        messages.success(self.request, 'Profile successfully updated.')
        return reverse_lazy('userprofile', kwargs={'username': self.request.user})


class UserProfileView(DetailView):
    slug_field = "user__username"  # Enables users to search by username
    slug_url_kwarg = "username"
    model = models.UserProfile
    template_name = "profiles/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_user = self.request.user
        other_user = self.get_object().user
        context['you_are_blocking'] = models.Block.objects.filter(blocker=main_user,
                                                                  blocked=other_user)
        context['you_are_blocked'] = models.Block.objects.filter(blocker=other_user,
                                                                 blocked=main_user)
        context['user_is_followed'] = models.Follow.objects.filter(followee=main_user,
                                                                   follower=other_user)
        context['user_is_following'] = models.Follow.objects.filter(followee=other_user,
                                                                    follower=main_user)
        context['mutual_follow'] = context['user_is_following'] and context['user_is_followed']
        return context


class UserSignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = "profiles/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully')
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        models.UserProfile.objects.create(user=User.objects.get(username=username))
        return response


# Functional Views


@login_required()
def block_user_view(request, *args, **kwargs):
    if request.method == "POST":
        to_user = User.objects.get(username=request.POST.get("to_user_username"))
        if models.Follow.objects.filter(followee=to_user, follower=request.user).exists():
            models.Follow.objects.get(followee=to_user, follower=request.user).delete()
        if models.Follow.objects.filter(followee=request.user, follower=to_user).exists():
            models.Follow.objects.get(followee=request.user, follower=to_user).delete()
        models.Block.objects.create(blocker=request.user, blocked=to_user)
        return HttpResponseRedirect(reverse_lazy("userprofile", kwargs={'username': request.user.username}))
    return HttpResponseRedirect(reverse_lazy("index"))


@login_required()
def unblock_user_view(request, *args, **kwargs):
    if request.method == "POST":
        to_user = User.objects.get(username=request.POST.get("to_user_username"))
        if models.Block.objects.filter(blocker=request.user, blocked=to_user).exists():
            models.Block.objects.get(blocker=request.user, blocked=to_user).delete()
        return HttpResponseRedirect(reverse_lazy("userprofile", kwargs={'username': to_user.username}))


@login_required()
def delete_follow_view(request, *args, **kwargs):
    if request.method == "POST":
        to_user_username = request.POST.get("to_user_username")
        to_user_instance = User.objects.get(username=to_user_username)
        instance_to_delete = models.Follow.objects.get(followee=to_user_instance, follower=request.user)
        instance_to_delete.delete()
        return HttpResponseRedirect(reverse_lazy("userprofile", kwargs={'username': to_user_username}))


@login_required()
def make_new_follow_view(request, *args, **kwargs):
    if request.method == "POST":
        to_user_username = request.POST.get("to_user_username")
        to_user_instance = User.objects.get(username=to_user_username)
        models.Follow.objects.create(followee=to_user_instance, follower=request.user)
        return HttpResponseRedirect(reverse_lazy("userprofile", kwargs={'username': to_user_username}))
    return HttpResponseRedirect(reverse_lazy("fail", kwargs={}))
