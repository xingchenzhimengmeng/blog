from django.urls import path
from . import views
app_name = 'ys'
urlpatterns = [
    path("home/", views.home, name="home"),
    path("user/<int:id_>/", views.user, name="user"),
    path("article/<int:id_>/", views.article, name="article"),
    path("delete/<int:id_>/article", views.delete_article, name="delete_article"),
    path("create/topic/", views.create_topic, name="create_topic"),
    path("write/", views.write, name="write"),
    path("edit/<int:id_>/", views.edit, name="edit"),
    path("like/article/<int:id_>/", views.like_article, name="like_article"),
    path("favorite/article/<int:id_>/", views.favorite_article, name="favorite_article"),

]
