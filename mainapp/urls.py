from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse
from mainapp import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('loutin/', views.LogoutView.as_view(), name='logout'),
]
