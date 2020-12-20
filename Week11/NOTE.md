## Django源码
### manage.py 源码
### URLconf 源码——偏函数
#### URLconf-URL调度器
#### partial 函数的实现
### view 源码——HttpRequest 与 HttpResponse
#### 请求与响应
#### QueryDict
### ORM 源码——元类
### Template 源码——render 方法的实现
### DjangoWeb相关功能
管理页面
表单与Auth
信号
中间件
Django管理页面
管理页面的设计哲学：
管理后台是一项缺乏创造性和乏味的工作，Django 全自动地根据模型创建后台界面。
管理界面不是为了网站的访问者，而是为管理者准备的。
创建管理员账号：
python manage.py createsuperuser
增加模型：
./index/admin.py

from .models import Type, Name
 注册模型
admin.site.register(Type)
admin.site.register(Name)
表单
<form action="result.html" method="post">
username:<input type="text" name="username" /><br>
password:<input type="password" name="password" /> <br>
<input type="submit" value="登录">
</form>
使用Form对象定义表单
# form.py
from django import forms
class LoginForm(forms.Form):
username = forms.CharField()
password = forms.CharField(widget=forms.PasswordInput, min_length=6)
<form action="/login2" method="post">
{% csrf_token %}
{{ form }}
<input type="submit" value="Login">
</form>
表单与内部auth功能结合
# python manage.py shell

>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('tom', 'tom@tom.com', 'tompassword')
>>> user.save()
>>> from django.contrib.auth import authenticate
>>> user = authenticate(username='tom', password='tompassword’)
auth功能
def login2(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 读取表单的返回值
                cd = login_form.cleaned_data 
                user = authenticate(username=cd['username'], password=cd['password'])
                if user:
                    # 登陆用户
                    login(request, user) 
                    return HttpResponse('登录成功')
                else:
                    return HttpResponse('登录失败')
信号
发生事件，通知应用程序
支持若干信号发送者通知一组接收者
解耦
内建信号有哪些？
https://docs.djangoproject.com/zh-hans/2.2/ref/signals/
信号怎么用？

# 函数方式注册回调函数
from django.core.signals import request_started
request_started.connect(my_callback1)

# 装饰器方式注册回调函数
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback2(sender, **kwargs):
    pass
中间件
Django中间件是什么？
全局改变输入或输出
轻量级的、低级的“插件”系统
对请求、响应处理的钩子框架
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class Middle1(MiddlewareMixin):
    def process_request(self,request):
        print('中间件请求')
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('中间件视图')
    def process_exception(self, request, exception):
        print('中间件异常')
    def process_response(self, request, response):
        print('中间件响应')
        return response
Django的其他功能
生产环境部署
定时任务
gunicorn
# 安装gunicorn
pip install gunicorn
# 在项目目录执行
gunicorn MyDjango.wsgi
Celery
Celery 是分布式消息队列
使用 Celery 实现定时任务
Redis 安装和启动
redis-server /path/to/redis.conf
安装 Celery
pip install celery
pip install redis==2.10.6
pip install celery-with-redis
pip install django-celery
添加app
django-admin startproject MyDjango
python manager.py startapp djcron

INSTALL_APPS=[
    'djcelery',
    'djcron'
]
迁移生成表
python manage.py migrate
配置django时区
from celery.schedules import crontab
from celery.schedules import timedelta
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://:123456@127.0.0.1:6379/' # 代理人
CELERY_IMPORTS = ('djcron.tasks') # app
CELERY_TIMEZONE = 'Asia/Shanghai' # 时区
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务调度器
在 MyDjango 下建立 celery.py
import os
from celery import Celery, platforms
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','MyDjango.settings')
app = Celery('MyDjango')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True
在 __init __.py 增加
# 使用绝对引入，后续使用import引入会忽略当前目录下的包
from __future__ import absolute_import
from .celery import app as celery_app
from MyDjango.celery import app

@app.task()
def task1():
    return 'test1'

@app.task()
def task2():
    return 'test2'

启动 Celery
celery -A MyDjango beat -l info
celery -A MyDjango worker -l info
通过 admin 增加定时任务
Flask
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
$ export FLASK_APP=hello.py
$ flask run
Flask的上下文与信号
上下文：request 上下文与 session 上下文
信号：Flask 从 0.6 开始，通过 Blinker 提供了信号支持
pip install blinker
Tornado
Tornado 的同步 IO 与异步 IO：
http_client = HTTPClient()
http_client = AsyncHTTPClient()
Tornado 路由映射
路由映射

application = tornado.web.Application([ 
    (r"/", MainHandler), 
])
Tornado 上下文
import tornado.ioloop
ioloop = tornado.ioloop.IOLoop.instance()
def callback():
    print('callback')
    
def async_task():
    ioloop.add_callback(callback=callback)