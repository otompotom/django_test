from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import generic

from . import forms

class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"