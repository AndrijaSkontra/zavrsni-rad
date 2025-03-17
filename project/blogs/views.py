from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Blog, Comment


# Create your views here.
def index(request):
    latest_blogs = Blog.objects.all()[:5]
    return render(request, "blogs/index.html", {"blogs": latest_blogs})


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog_comments = blog.comment_set.all()
    return render(request, "blogs/detail.html", {"blog": blog, "comments": blog_comments})


def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if (request.method == "GET"):
        return render(request, "comments/add.html")
