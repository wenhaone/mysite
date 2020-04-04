from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from user.models import User



class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 统一验证登录
        # return none 或者 不写return才会继续往下执行, 不需要执行
        if request.path == '/user/login/' or request.path == '/user/regist/':
            return None
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect('/user/login/')

        users = User.objects.filter(u_ticket=ticket)
        if not users:
            return HttpResponseRedirect('/user/login/')
# 将user赋值在request请求的user上，以后可以直接判断user有没有存在
# 备注，django自带的有user值
        request.user = users[0]