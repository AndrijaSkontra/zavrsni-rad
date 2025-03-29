# This file is generated with OpenAI o3-mini-high model

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Blog, Comment, CommentVote


def list_blogs(request):
    blogs = Blog.objects.all()
    return render(request, "blogs/blog_list.html", {"blogs": blogs})


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, "blogs/blog_detail.html", {"blog": blog})


@login_required
@require_POST
def add_comment(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    content = request.POST.get("content")

    if not content:
        messages.error(request, "Comment content is required.")
        return redirect("blogs:blog_detail", slug=slug)

    comment = Comment.objects.create(
        blog=blog,
        user=request.user,
        content=content
    )

    if request.headers.get("HX-Request"):
        return render(request, "blogs/partial_comment.html", {"comment": comment})
    return redirect("blogs:blog_detail", slug=slug)


@login_required
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
    
    try:
        # Try to create a new vote
        CommentVote.objects.create(
            comment=comment,
            user=request.user,
            vote=vote_value
        )
    except IntegrityError:
        # User has already voted, update their vote
        vote = CommentVote.objects.get(comment=comment, user=request.user)
        if vote.vote == vote_value:
            # If clicking the same vote type, remove the vote
            vote.delete()
        else:
            # Change the vote
            vote.vote = vote_value
            vote.save()

    return render(
        request,
        "blogs/partial_comment_vote.html",
        {
            "comment": comment,
            "user_vote": comment.get_user_vote(request.user)
        }
    )
