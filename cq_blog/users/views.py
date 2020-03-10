from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from users.models import BlogUser
from random import Random
from django.core.mail import send_mail
from .models import EmailVerifyRecord
from  cq_blog.settings import EMAIL_FROM


# 生成随机字符串
def make_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送邮件
def my_send_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = make_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "博客-注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, 'login.html', {'error_msg': '用户未激活！'})
        else:
            return render(request, 'login.html', {'error_msg': '用户名或者密码错误！'})


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        print('asdfffffffffffffffffffffffffffffffffffffffff')
        print(active_code)
        print(all_records)
        print('ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
        if all_records:
            for record in all_records:
                email = record.email
                user = BlogUser.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # 判断用户的EMAIL是否已存在
        if BlogUser.objects.filter(email=username):
            return render(request, "register.html", {"msg": "用户已存在"})
        user = BlogUser()
        user.username = username
        user.password = make_password(password)
        user.email = email
        user.is_active = False
        user.save()
        my_send_email(email, 'register')

        return render(request, 'login.html')
