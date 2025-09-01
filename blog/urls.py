from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "blog"

urlpatterns = [
    # Blog posts
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("post/<slug:slug>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),

    # Auth
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="blog:post_list"), name="logout"),
]
