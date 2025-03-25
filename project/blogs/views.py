# This file is generated with OpenAI o3-mini-high model
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Blog, Comment, CommentVote


def list_blogs(request):
    blogs = Blog.objects.all()
    return render(request, "blogs/blog_list.html", {"blogs": blogs})


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, "blogs/blog_detail.html", {"blog": blog})


@require_POST
def add_comment(request, slug):
    if not request.user.is_authenticated:
        print("this is where the request will fail HERE WATCH ME")
        return HttpResponse("Login first", status=401)

    blog = get_object_or_404(Blog, slug=slug)
    guest_name = request.POST.get("guest_name")
    content = request.POST.get("content")

    comment = Comment.objects.create(blog=blog, guest_name=guest_name, content=content)

    if request.headers.get("HX-Request"):
        return render(request, "blogs/partial_comment.html", {"comment": comment})
    return redirect("blogs:blog_detail", slug=slug)


@require_POST
def vote_comment(request, comment_id):
    vote_str = request.POST.get("vote")
    try:
        vote_value = int(vote_str)
    except (TypeError, ValueError):
        vote_value = 0

    if vote_value not in (1, -1):
        return HttpResponse(status=400)

    comment = get_object_or_404(Comment, id=comment_id)
    CommentVote.objects.create(comment=comment, vote=vote_value)

    return render(request, "blogs/partial_comment_vote.html", {"comment": comment})


def profile(request):
    return render(request, "registration/profile.html")


def logout_view(request):
    logout(request)
    return render(request, "registration/login.html")
