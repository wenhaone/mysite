from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('regist/', views.RegistView.as_view(), name='regist'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),


    ]