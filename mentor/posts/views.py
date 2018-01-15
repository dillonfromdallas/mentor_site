from . import models
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

# Create your views here.


class PostCreateView(LoginRequiredMixin, CreateView):
    fields = ['message']
    model = models.UserProfilePost
    slug_field = "user__username"
    slug_url_kwarg = 'username'
    template_name = "posts/create_post.html"

    def get_success_url(self):
        messages.success(self.request, 'Post created.')
        return reverse_lazy('userprofile', kwargs={'username': self.request.user})



class PostFocusView(DetailView):
    model = models.UserProfilePost


def test_view(request, **kwargs):
    return HttpResponse("View accessed successfully.")
