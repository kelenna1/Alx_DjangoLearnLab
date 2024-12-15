from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class PostAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create a test post
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.user
        )

    def test_create_post(self):
        data = {"title": "New Post", "content": "This is a new post."}
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "New Post")

    def test_retrieve_posts(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["results"]) > 0)

    def test_update_post(self):
        data = {"title": "Updated Post", "content": "Updated content."}
        response = self.client.put(f"/api/posts/{self.post.id}/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Updated Post")

    def test_delete_post(self):
        response = self.client.delete(f"/api/posts/{self.post.id}/")
        self.assertEqual(response.status_code, 204)

