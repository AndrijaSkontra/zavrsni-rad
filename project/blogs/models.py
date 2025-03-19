from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    negative_count = models.IntegerField(default=0)
    positive_count = models.IntegerField(default=0)


# todo run migrations
class CommentResponse(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    RESPONSE_CHOICES = [
        ("PO", "Positive"),
        ("NE", "Negative")
    ]

    response = models.CharField(
        max_length=2,
        choices=RESPONSE_CHOICES,
    )
