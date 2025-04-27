from django.urls import path
from . import views
app_name = 'app01'
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # path("user/list/", views.user_list, name="list"),
    path("user/add/", views.user_add, name="user_add"),
    # path("user/<int:id_>/delete/", views.user_delete, name="user_delete"),
    # path("user/<int:id_>/edit/", views.user_edit, name="user_edit"),
]