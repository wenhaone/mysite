from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect,response
from django.urls import  reverse
from .models import User
import random
import time
from  django.template import loader

from django.contrib.auth.hashers import make_password,check_password
# Create your views here.

class IndexView(View):
    def get(self,request):
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return
        if User.objects.filter(u_ticket=ticket).exists():
            stuinfos = User.objects.all()
            return render(request,'user/index.html',{'stuinfos':stuinfos})
        else:
            return HttpResponseRedirect('user/login.html')

class RegistView(View):
    def get(self,request):
        return render(request,'user/regist.html')
    def post(self,request):
        name = request.POST.get("name")
        print(name)
        password = request.POST.get("password")
        print(password)
        password = make_password(password)

        User.objects.create(u_name=name,u_password=password)

        return HttpResponseRedirect('user/login')
        # return render(request,'user/index.html')

class LoginView(View):
    def get(self,request):
        return render(request,'user/login.html')
    def post(self,request):
        name = request.POST.get('name')
        password = request.POST.get('password')
        #查询用户是否在数据库中
        print(name , password)
        if User.objects.filter(u_name = name).exists():
            user = User.objects.get(u_name =name)
            if check_password(password,user.u_password):
                ticket = ''
                for i in range(15):
                    s = 'abcdefghijklmnopqrstuvwxyz'
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK' + ticket + str(now_time)
                response = HttpResponseRedirect(reverse('user:index'))
                #绑定令牌到cookie里面
                # max_age : 存活时间
                response.set_cookie('ticket',ticket,max_age=10000)

                user.u_ticket = ticket
                user.save()
                return response
            else:
                return render(request,'user/login.html',{'msgerror':'用户名密码错误'})
        else:
            return render(request,'user/login.html',{'msgerror':'用户名不存在'})

class LogoutView(View):
    def get(self,request):
        response =  HttpResponseRedirect(reverse('user:index'))
        response.delete_cookie('ticket')
        return response