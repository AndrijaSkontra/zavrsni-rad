from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Blog, Comment, CommentResponse


# Create your views here.
def index(request):
    latest_blogs = Blog.objects.all()[:5]
    return render(request, "blogs/index.html", {"blogs": latest_blogs})


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog_comments = blog.comment_set.all()
    return render(request, "blogs/detail.html", {"blog": blog, "comments": blog_comments})


def add_comment(request, blog_id):
    if (request.method == "GET"):
        return render(request, "comments/add.html")
    if (request.method == "POST"):
        blog = get_object_or_404(Blog, pk=blog_id)
        comment_content = request.POST.get("content")
        if (comment_content == ""):
            return render(request, "comments/invalid.html")
        comment = Comment()
        comment.content = comment_content
        comment.blog = blog
        comment.save()
        return redirect(f"/blogs/{blog_id}")


def add_good_response(request, comment_id, blog_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    response = CommentResponse()
    response.response = "PO"
    response.comment = comment
    response.save()
    comment.positive_count = comment.commentresponse_set.filter(response="PO").count()
    comment.save()
    return detail(request, blog_id)


def add_bad_response(request, comment_id, blog_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    response = CommentResponse()
    response.response = "NE"
    response.comment = comment
    response.save()
    comment.negative_count = comment.commentresponse_set.filter(response="NE").count()
    comment.save()
    return detail(request, blog_id)
