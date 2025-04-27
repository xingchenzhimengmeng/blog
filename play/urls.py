from django.urls import path
from . import views
app_name = 'play'
urlpatterns = [
    path("index/", views.index, name="index"),
    path("article/<int:id_>/", views.article, name="article"),
]
