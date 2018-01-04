from . import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView

# Create your views here.


class HomeIndexView(TemplateView):
    template_name = "profiles/index.html"


class UserProfileView(DetailView):
    slug_field = "username"
    slug_url_kwarg = slug_field
    model = models.UserProfile
    template_name = "profiles/user_profile.html"


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
