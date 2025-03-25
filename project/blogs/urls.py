# This file is generated with OpenAI o3-mini-high model
from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [
    path("", views.list_blogs, name="blog_list"),
    path("logout/", views.logout_view, name="logout"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("<slug:slug>/add_comment/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/vote/", views.vote_comment, name="vote_comment"),
]
