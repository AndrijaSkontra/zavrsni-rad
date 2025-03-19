from django.urls import path

from . import views

app_name = "blogs"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:blog_id>/", views.detail, name="detail"),
    path("<int:blog_id>/comments/add/", views.add_comment, name="add_comment"),
    path("<int:blog_id>/comments/<int:comment_id>/good", views.add_good_response, name="good_response"),
    path("<int:blog_id>/comments/<int:comment_id>/bad", views.add_bad_response, name="bad_response"),
]
