# This file is generated with OpenAI o3-mini-high model

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The admin user who created the blog post",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,  # Allow null temporarily for existing comments
        blank=True
    )
    guest_name = models.CharField(max_length=100, null=True, blank=True)  # Keep this temporarily for existing comments
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        name = self.user.username if self.user else self.guest_name
        return f"Comment by {name} on {self.blog.title}"

    @property
    def vote_total(self):
        """
        Returns the net total of votes (upvotes minus downvotes)
        for the comment.
        """
        total = self.votes.aggregate(total=models.Sum("vote")).get("total")
        return total if total is not None else 0

    def get_user_vote(self, user):
        """
        Returns the user's vote for this comment, if any.
        """
        if not user.is_authenticated:
            return None
        vote = self.votes.filter(user=user).first()
        return vote.vote if vote else None


class CommentVote(models.Model):
    VOTE_CHOICES = (
        (1, "Upvote"),
        (-1, "Downvote"),
    )
    comment = models.ForeignKey(
        Comment, related_name="votes", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_votes",
        null=True,  # Allow null temporarily
        blank=True
    )
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment Vote"
        verbose_name_plural = "Comment Votes"
        # Ensure one vote per user per comment
        unique_together = ['comment', 'user']

    def __str__(self):
        username = self.user.username if self.user else "Unknown"
        return f"Vote {self.vote} by {username} on Comment {self.comment.id}"
