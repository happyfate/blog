"""cq_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blogs import views
from blogs.views import SearchView, blog_list,blog_detail,CommentView
from users.views import LoginView, RegisterView, ActiveView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),    #找到以admin开头的页面
    path('', views.index, name='index'),
    path('search/', SearchView.as_view(), name='search'),
    path('list/', blog_list, name='blog_list'),
    re_path('category/(?P<cid>[0-9])/', blog_list, name='category'),     #django3.04版本正则表达式不要用path，用re_path
    re_path('tags/(?P<tid>[0-9])/', blog_list, name='tags'),
    re_path('blog/(?P<bid>[0-9])/', blog_detail, name='blog_detail'),
    re_path('comment/(?P<bid>[0-9])/', CommentView.as_view(), name='comment'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    re_path('active/(?P<active_code>[a-zA-Z0-9]+)', ActiveView.as_view(), name='active'),   #注意，这里一定要有‘+’，要不然返回的active_code只有一个首字母
    path('logout/', LogoutView.as_view(), name='logout'),
]
