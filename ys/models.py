from django.db import models
from app01.models import User
import markdown
# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=50, unique=True)       # 话题

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)                    # 帖子标题
    content = models.TextField()                                # 帖子内容
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 帖子作者
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)     # 话题
    created_at = models.DateTimeField(auto_now_add=True)        # 创建时间
    updated_at = models.DateTimeField(auto_now=True)             # 更新时间
    picture = models.TextField(default='', null=True)           # 图片
    @property
    def f_content(self):
        return markdown.markdown(self.content, extensions=['fenced_code'])

    @property
    def f_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def f_updated_at(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def f_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')
