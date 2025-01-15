import string
from django.shortcuts import render,redirect,reverse
from django.http.response import JsonResponse
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

@require_http_methods(['GET', 'POST'])
def kunlogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登录
                login(request, user)
                user.is_authenticated
                # 判断是否需要记住我
                if not remember:
                    # 设置过期时间
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print("邮箱or密码错误")
                # form.add_error('email', '邮箱和密码错误！')
                # return render(request, 'login.html', context={'form': form})
                return redirect(reverse('kunauth:login'))

def kunlogout(request):
    logout(request)
    return redirect('/')

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(
                email=email, username=username, password=password
            )
            return redirect(reverse('kunauth:login'))
        else:
            print(form.errors)
            #重新跳转到登录的界面
            return redirect(reverse('kunauth:register'))
            # return render(request, 'register.html', {'form': form})



def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": '必须传递邮箱！'})
    #生成验证码（取四位阿拉伯数字）
    captcha = "".join(random.sample(string.digits,4))
    #存储到数据库中
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail("kunkun博客注册验证码", message=f"欢迎IKUN or 小黑子 or 纯鹿人，您的注册验证码是：{captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！"})