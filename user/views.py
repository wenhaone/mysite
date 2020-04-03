from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import  reverse
from .models import User
from  django.template import loader
# Create your views here.

class IndexView(View):
    def get(self,request):
        return render(request,"user/index.html")

class RegistView(View):
    def get(self,request):
        return render(request,'user/regist.html')
    def post(self,request):
        name = request.POST.get("name")
        print(name)
        password = request.POST.get("password")
        User.u_name = name
        User.u_password = password

        return render(request,'user/index.html')



class LogoutView(View):
    def get(self,request):
        return HttpResponseRedirect(reverse('user:index'))