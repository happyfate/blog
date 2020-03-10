from datetime import datetime
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import Banner
from .models import Post
from .models import BlogCategroy
from .models import Comment
from .models import FriendlyLink
from .models import Tags
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

#评论
class CommentView(View):
    def get(self, request):
        pass
    def post(self, request, bid):

        comment = Comment()
        #取数据
        comment.user = request.user
        comment.post = Post.objects.get(id=bid) #评论的文章
        comment.content = request.POST.get('content')
        comment.pub_date = datetime.now()
        comment.save()
        # Ajax
        return HttpResponseRedirect(reverse("blog_detail", kwargs={"bid":bid})) #跳转到blog_detail

#博客详细
def blog_detail(request, bid):
    post = Post.objects.get(id=bid)

    #记录浏览量
    post.views += 1
    post.save(update_fields=['views'])

    # 最新评论
    new_comment_list = Comment.objects.order_by('pub_date').all()[:6]
    comment_list = post.comment_set.all()
    # 去重
    new_comment_list1 = []
    post_list1 = []
    for c in new_comment_list:
        if c.post.id not in post_list1:
            new_comment_list1.append(c)
            post_list1.append(c.post.id)

    #博客标签列表
    tag_list = post.tags.all()

    #相关推荐（标签相同的）
    post_recommend_list = set(Post.objects.filter(tags__in=tag_list)[:6])

    ctx = {
        'post': post,
        'new_comment_list1': new_comment_list1,
        'post_recommend_list': post_recommend_list,
        'comment_list':comment_list
    }
    return render(request, 'show.html', ctx)



# 搜索
class SearchView(View):
    def get(self, request):
        pass

    def post(self, request):
        keywords = request.POST.get('keyword')
        post_list = Post.objects.filter(Q(title__icontains=keywords) | Q(content__icontains=keywords))
        ctx = {
            'post_list': post_list
        }

        return render(request, 'list.html', ctx)


# 标签云
class TagMessage(object):
    def __init__(self, tid, name, count):
        self.tid = tid
        self.name = name
        self.count = count


# 博客列表
def blog_list(request, cid=-1, tid=-1):
    post_list = None
    if cid != -1:
        cat = BlogCategroy.objects.get(id=cid)
        post_list = cat.post_set.all()
    elif tid != -1:
        tag = Tags.objects.get(id=tid)
        post_list = tag.post_set.all()
    else:
        post_list = Post.objects.all()

    #分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(post_list, per_page=5, request=request)
    post_list = p.page(page)



    tags = Tags.objects.all()
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tm = TagMessage(t.id, t.name, count)
        tag_message_list.append(tm)

    new_comment_list = Comment.objects.order_by('-pub_date').all()[:5]  # list.html最新评论
    new_comment_list1 = []
    post_list1 = []
    for c in new_comment_list:
        if c.post.id not in post_list1:
            new_comment_list1.append(c)
            post_list1.append(c.post.id)


    ctx = {
        'post_list': post_list,
        'tags': tag_message_list,
        'new_comment_list': new_comment_list1,
    }
    return render(request, 'list.html', ctx)


# 视图函数 HTTPRequest
def index(request):
    banner_list = Banner.objects.all()
    recommend_lsit = Post.objects.filter(recommend=1)  # 1表示真，表示这篇文章为推荐文章
    post_list = Post.objects.order_by('-pub_date').all()[:6]    #最新博客
    blogcategroy_list = BlogCategroy.objects.all()  # 博客分类


    new_comment_list = Comment.objects.order_by('-pub_date').all()[:5]  # 最新评论
    links = FriendlyLink.objects.all()

    # 去重
    new_comment_list1 = []
    post_list1 = []
    for c in new_comment_list:
        if c.post.id not in post_list1:
            new_comment_list1.append(c)
            post_list1.append(c.post.id)

    # 分页功能
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(post_list, per_page=3, request=request)

    post_list = p.page(page)

    ctx = {
        'banner_list': banner_list,
        'recommend_lsit': recommend_lsit,
        'post_list': post_list,
        'blogcategroy_lsit': blogcategroy_list,
        'new_comment_list': new_comment_list1,
        'links': links

    }
    return render(request, 'index.html', ctx)
