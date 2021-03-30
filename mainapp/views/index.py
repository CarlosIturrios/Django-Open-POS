from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views
from django.views.generic import TemplateView


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'mainapp/template.html'


class LoginView(views.LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/login.html'


class LogoutView(views.LogoutView):
    pass
