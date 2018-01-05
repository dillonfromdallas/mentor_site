from . import models
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView


# Create your views here.


class HomeIndexView(TemplateView):
    template_name = "profiles/index.html"


class UserProfileView(DetailView):
    slug_field = "username"  # Enables users to search by username
    slug_url_kwarg = slug_field
    model = User
    template_name = "profiles/user_profile.html"

    def get_object(self, queryset=None):
        '''Takes the username input, finds a matching User object, and creates/delivers a UserProfile in it's place.'''
        user = super().get_object()  # Ensures this only works with existing User objects.
        try:
            profile = models.UserProfile.objects.get(user=user)
            return profile
        except ObjectDoesNotExist:
            profile = models.UserProfile.objects.create(user=user)
            profile.save()
            return profile


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
        return response
