from django.urls import path
from . import views

app_name = 'kunauth'

urlpatterns = [
    path('login', views.kunlogin, name='login'),
    path('logout', views.kunlogout, name='logout'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email_captcha'),
]