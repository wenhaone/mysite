from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect,response
from django.urls import  reverse
from .models import User
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
import random
import time
from  django.template import loader

from django.contrib.auth.hashers import make_password,check_password
# Create your views here.

class IndexView(View):
    def get(self,request):
        print(request.user.username)
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
        username = request.POST.get("name")
        print(username)
        password = request.POST.get("password")
        print(password)
        # password = make_password(password)
#校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            user = None
        if user:
            return render(request,'user/regist.html',{'errmsg':'用户名已存在'})

        User.objects.create_user(username,password)
        return HttpResponseRedirect('user/login')
        # return render(request,'user/index.html')
from django.contrib import auth

class LoginView(View):
    def get(self,request):
        return render(request,'user/login.html')
    def post(self,request):
        #1、接收数据、2、校验数据
        #3、登录校验 4、返回应答
        name = request.POST.get('name')
        password = request.POST.get('password')

        if not all([name,password]):
            return render(request,'user/login.html',{'msgerr':'参数不完整'})
        #如果验证成功，返回的是一个用户对象 否则为返回的是匿名用户，所有为空
        user = auth.authenticate(username=name,password=password)
        if user:
            #将用户封装到 request.user中
            auth.login(request,user)
            return HttpResponseRedirect(reverse('user:index'))
        else:
            return HttpResponseRedirect(reverse('user:login'))
        # #查询用户是否在数据库中
        # print(name , password)
        # if User.objects.filter(u_name = name).exists():
        #     user = User.objects.get(u_name =name)
        #     if check_password(password,user.u_password):
        #         ticket = ''
        #         for i in range(15):
        #             s = 'abcdefghijklmnopqrstuvwxyz'
        #             ticket += random.choice(s)
        #         now_time = int(time.time())
        #         ticket = 'TK' + ticket + str(now_time)
        #         response = HttpResponseRedirect(reverse('user:index'))
        #         #绑定令牌到cookie里面
        #         # max_age : 存活时间
        #         response.set_cookie('ticket',ticket,max_age=10000)
        #
        #         user.u_ticket = ticket
        #         user.save()
        #         return response
        #     else:
        #         return render(request,'user/login.html',{'msgerror':'用户名密码错误'})
        # else:
        #     return render(request,'user/login.html',{'msgerror':'用户名不存在'})

class LogoutView(View):
    """退出登录"""
    def get(self,request):
        #清除用户session信息
        logout(request)
        # response =  HttpResponseRedirect(reverse('user:index'))
        # response.delete_cookie('ticket')
        return response
        return HttpResponseRedirect('user/index')