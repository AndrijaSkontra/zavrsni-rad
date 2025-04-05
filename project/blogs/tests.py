from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Blog, Comment, CommentVote


class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='complex_password123'
        )
        
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            content='This is a test blog content',
            author=self.user
        )
        
    def test_blog_creation(self):
        self.assertEqual(self.blog.title, 'Test Blog')
        self.assertEqual(self.blog.slug, 'test-blog')
        self.assertEqual(self.blog.content, 'This is a test blog content')
        self.assertEqual(self.blog.author, self.user)
        
    def test_blog_str_method(self):
        self.assertEqual(str(self.blog), 'Test Blog')


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='complex_password123'
        )
        
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            content='This is a test blog content',
            author=self.user
        )
        
        self.comment = Comment.objects.create(
            blog=self.blog,
            user=self.user,
            content='This is a test comment'
        )
        
    def test_comment_creation(self):
        self.assertEqual(self.comment.blog, self.blog)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, 'This is a test comment')
        
    def test_comment_str_method(self):
        expected_str = f"Comment by {self.user.username} on {self.blog.title}"
        self.assertEqual(str(self.comment), expected_str)
        
    def test_vote_total_property(self):
        # Initially no votes
        self.assertEqual(self.comment.vote_total, 0)
        
        # Add an upvote
        CommentVote.objects.create(
            comment=self.comment,
            user=self.user,
            vote=1
        )
        self.assertEqual(self.comment.vote_total, 1)
        
    def test_get_user_vote_method(self):
        # Initially no vote
        self.assertIsNone(self.comment.get_user_vote(self.user))
        
        # Add a vote
        CommentVote.objects.create(
            comment=self.comment,
            user=self.user,
            vote=1
        )
        self.assertEqual(self.comment.get_user_vote(self.user), 1)


class BlogViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='complex_password123'
        )
        
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            content='This is a test blog content',
            author=self.user
        )
        
        self.list_url = reverse('blogs:blog_list')
        self.detail_url = reverse('blogs:blog_detail', args=['test-blog'])
        
    def test_list_blogs_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blog_list.html')
        self.assertContains(response, 'Test Blog')
        
    def test_blog_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blog_detail.html')
        self.assertContains(response, 'Test Blog')
        self.assertContains(response, 'This is a test blog content')
        
    def test_add_comment_view_authenticated(self):
        self.client.login(username='testuser', password='complex_password123')
        response = self.client.post(
            reverse('blogs:add_comment', args=['test-blog']),
            {'content': 'This is a test comment'}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful comment
        self.assertEqual(Comment.objects.count(), 1)
        
    def test_add_comment_view_unauthenticated(self):
        response = self.client.post(
            reverse('blogs:add_comment', args=['test-blog']),
            {'content': 'This is a test comment'}
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertEqual(Comment.objects.count(), 0)
        

from django.test import TestCase, Client, TransactionTestCase

class CommentVoteViewTests(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        # Clear any existing votes to avoid test interference
        CommentVote.objects.all().delete()
        Comment.objects.all().delete()
        Blog.objects.all().delete()
        User.objects.all().delete()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='complex_password123'
        )
        
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            content='This is a test blog content',
            author=self.user
        )
        
        self.comment = Comment.objects.create(
            blog=self.blog,
            user=self.user,
            content='This is a test comment'
        )
        
        self.vote_url = reverse('blogs:vote_comment', args=[self.comment.id])
    
    def tearDown(self):
        # Make sure to log out after each test
        self.client.logout()
        
    def test_vote_comment_authenticated_upvote(self):
        self.client.login(username='testuser', password='complex_password123')
        response = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CommentVote.objects.count(), 1)
        self.assertEqual(CommentVote.objects.first().vote, 1)
        self.client.logout()
        
    def test_vote_comment_authenticated_downvote(self):
        # Use a different user to avoid unique constraint violation
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='complex_password123'
        )
        self.client.login(username='testuser2', password='complex_password123')
        response = self.client.post(self.vote_url, {'vote': '-1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CommentVote.objects.filter(user=user2).count(), 1)
        vote = CommentVote.objects.get(user=user2)
        self.assertEqual(vote.vote, -1)
        self.client.logout()
        
    def test_vote_comment_unauthenticated(self):
        response = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertEqual(CommentVote.objects.count(), 0)
        
    def test_vote_comment_toggle(self):
        # Create a new user for this test
        user3 = User.objects.create_user(
            username='testuser3',
            email='test3@example.com',
            password='complex_password123'
        )
        self.client.login(username='testuser3', password='complex_password123')
        
        # First vote (upvote)
        response1 = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(CommentVote.objects.filter(user=user3).count(), 1)
        vote = CommentVote.objects.get(user=user3)
        self.assertEqual(vote.vote, 1)
        
        # Click again to toggle/remove the vote
        response2 = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(CommentVote.objects.filter(user=user3).count(), 0)
        self.client.logout()
        
    def test_vote_comment_change(self):
        # Create a new user for this test
        user4 = User.objects.create_user(
            username='testuser4',
            email='test4@example.com',
            password='complex_password123'
        )
        self.client.login(username='testuser4', password='complex_password123')
        
        # First vote (upvote)
        response1 = self.client.post(self.vote_url, {'vote': '1'})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(CommentVote.objects.filter(user=user4).count(), 1)
        vote = CommentVote.objects.get(user=user4)
        self.assertEqual(vote.vote, 1)
        
        # Change to downvote
        response2 = self.client.post(self.vote_url, {'vote': '-1'})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(CommentVote.objects.filter(user=user4).count(), 1)
        vote = CommentVote.objects.get(user=user4)
        self.assertEqual(vote.vote, -1)
        self.client.logout()
