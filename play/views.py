from django.shortcuts import render, redirect
from django.http import HttpResponse
from ys import models
from django.db.models import Q
# Create your views here.


def index(request):
    search = request.GET.get('search')
    if search:
        posts = models.Post.objects.filter(
            Q(title__contains=search) | Q(author__name__contains=search) | Q(content__contains=search))
    else:
        posts = models.Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def article(request, id_):
    post = models.Post.objects.filter(id=id_)
    if not post:
        return HttpResponse('文章不存在')
    post = post.first()
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
    if request.session.get('info') and post.author.id == request.session['info']['id']:
        form['flag'] = True
    return render(request, 'open_article.html', form)
