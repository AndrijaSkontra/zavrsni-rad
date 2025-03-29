import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from blogs.models import Comment, CommentVote

# Delete all comments and votes
CommentVote.objects.all().delete()
Comment.objects.all().delete()

print("All comments and votes have been deleted.")
