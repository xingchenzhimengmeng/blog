from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
import os
from django.db.models import Q
# from django import forms
# from .models import Video
from pathlib import Path
# Create your views here.

from datetime import datetime
from pathlib import Path
BASE_DIR = str(Path(__file__).resolve().parent.parent)
def get_safe_filename():
    # 获取当前时间
    now = datetime.now()
    # 格式化时间为字符串，包含年月日时分秒
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    # 替换非法字符（如空格和冒号）为合法字符（如下划线）
    safe_filename = time_str.replace(" ", "_").replace(":", "-")
    return safe_filename

def create_topic(request):
    if request.method == 'GET':
        return render(request, 'create_topic.html')
    form = {
        'title': request.POST['title'],
    }
    result2 = models.Topic.objects.filter(**form)
    if result2:
        form['tip'] = '话题已存在'
        return render(request, 'create_topic.html', form)
    models.Topic.objects.create(**form)
    return redirect('ys:create_topic')


def home(request):
    search = request.GET.get('search')
    if search:
        posts = models.Post.objects.filter(Q(title__contains=search) | Q(author__name__contains=search) | Q(content__contains=search))
    else:
        posts = models.Post.objects.all()
    user = models.User.objects.get(id=request.session['info']['id'])
    return render(request, 'home.html', {'posts': posts, 'user': user})


def write(request):
    if request.method == 'GET':
        topics = models.Topic.objects.all()
        form = {'topics': topics}
        return render(request, 'write.html', form)

    form = {
        'title': request.POST['title'],
        'content': request.POST['content'],
        'picture': '#',
    }
    # 话题
    topic = models.Topic.objects.filter(id=request.POST['topic_id'])
    if topic:
        form['topic'] = topic.first()
    # 作者
    form['author'] = models.User.objects.filter(id=request.session['info']['id']).first()
    # print(form)
    obj = models.Post.objects.create(**form)
    print(obj.id)
    # 封面
    picture = request.FILES.get('picture')
    if picture:

        pic_dir = BASE_DIR+ '/static/images/' + str(obj.id)
        obj.picture = 'images/'+str(obj.id)+'.jpg'
        obj.save()
        with open(pic_dir + '.jpg', 'wb+') as f:
            for chunk in picture.chunks():
                f.write(chunk)
    return redirect('ys:article', id_=obj.id)


def edit(request, id_):
    post2 = models.Post.objects.filter(id=id_)
    if not post2:
        return HttpResponse('文章不存在')
    post = post2.first()
    if request.session['info']['id'] != post.author.id:
        return HttpResponse('无权编辑该文章')
    topics = models.Topic.objects.all()
    form = {
        'topics': topics,
        'post': post,
    }
    if request.method == 'GET':
        return render(request, 'write.html', form)
    if not request.POST['title'] or not request.POST['content']:
        return HttpResponse('文章缺失标题或内容')
    post.title = request.POST['title']
    post.content = request.POST['content']
    # 话题
    topic = models.Topic.objects.filter(id=request.POST['topic_id'])
    if topic:
        post.topic = topic.first()
    # 封面
    picture = request.FILES.get('picture')
    post.save()
    if picture:
        pic_dir = BASE_DIR+ '/static/' + post.picture
        if os.path.exists(pic_dir):
            os.remove(pic_dir)
        post.picture = "images/" + str(post.id) + get_safe_filename() + '.jpg'
        post.save()
        pic_dir = BASE_DIR+ '/static/' + post.picture
        with open(pic_dir, 'wb+') as f:
            for chunk in picture.chunks():
                f.write(chunk)
    return redirect('ys:article', id_=post.id)


def article(request, id_):
    post = models.Post.objects.filter(id=id_)
    if not post:
        return HttpResponse('文章不存在')
    post = post.first()
    if request.method == 'GET':
        comments = models.Comment.objects.filter(post=post)
        like_nums = models.Like.objects.filter(post=post).count()
        favorite_nums = models.Favorite.objects.filter(post=post).count()
        form = {
            'post': post,
            'comments': comments,
            'flag': False,
            'like_nums': like_nums,
            'favorite_nums': favorite_nums,
        }
        # print(post.author.id, request.session['info']['id'])
        if post.author.id == request.session['info']['id']:
            form['flag'] = True
        return render(request, 'article.html', form)
    comment_ = request.POST['comment']
    user_ = models.User.objects.filter(id=request.session['info']['id']).first()
    models.Comment.objects.create(user=user_, post=post, content=comment_)
    url = request.build_absolute_uri()
    return redirect(url)


def delete_article(request, id_):
    post2 = models.Post.objects.filter(id=id_)
    if not post2:
        return HttpResponse('文章不存在')
    post = post2.first()
    if request.session['info']['id'] != post.author.id:
        return HttpResponse('无权删除该文章')
    if len(post.picture)<100:
        pic_dir = BASE_DIR+ '/static/' + post.picture
        if os.path.exists(pic_dir):
            os.remove(pic_dir)
    post2.delete()
    return redirect('ys:home')


def like_article(request, id_):
    post = models.Post.objects.filter(id=id_)
    if not post:
        return HttpResponse('error')
    post = post.first()
    user = models.User.objects.filter(id=request.session['info']['id']).first()
    form = {
        'post': post,
        'user': user,
    }
    result = models.Like.objects.filter(**form)
    if result:
        result.delete()
        return HttpResponse("cancel_success")
    models.Like.objects.create(**form)
    return HttpResponse("like_success")


def favorite_article(request, id_):
    post = models.Post.objects.filter(id=id_)
    if not post:
        return HttpResponse('error')
    post = post.first()
    user = models.User.objects.filter(id=request.session['info']['id']).first()
    form = {
        'post': post,
        'user': user,
    }
    result = models.Favorite.objects.filter(**form)
    if result:
        result.delete()
        return HttpResponse("cancel_success")
    models.Favorite.objects.create(**form)
    return HttpResponse("collect_success")


def user(request, id_):
    user = models.User.objects.filter(id=id_)
    if not user:
        return HttpResponse('用户不存在')
    user = user.first()
    favorites = models.Favorite.objects.filter(user=user)

    form = {
        'user': user,
        'posts': models.Post.objects.filter(author=user),
        'favorites': favorites,
    }
    return render(request, 'user_index.html', form)

