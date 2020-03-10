from django.contrib import admin
from blogs.models import Banner
from blogs.models import Post, BlogCategroy, Tags, FriendlyLink
# Register your models here.

admin.site.register(Banner) #注册轮播图（后台有效）
# admin.site.register(Post)
admin.site.register(BlogCategroy)   #注册博客分类
admin.site.register(Tags)   #注册标签
admin.site.register(FriendlyLink)   #注册友情链接

class PostAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/editor/kindeditor-all.js',
            'js/editor/config.js',
        )
admin.site.register(Post, PostAdmin)    #注册最新博客
