
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')  # Log in as the test user

        # Sample book data
        self.book_data = {
            "title": "Test Book",
            "author": "Author Name",
            "publication_year": "2024-01-01"
        }
        
        # Create a book for testing update and delete
        self.book = Book.objects.create(
            title="Existing Book",
            author="Existing Author",
            published_date="2023-01-01"
        )

    # Test listing books
    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)  # Check if the response is a list

    # Test creating a book
    def test_create_book(self):
        response = self.client.post('/api/books/', self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.book_data['title'])

    # Test creating a book without authentication
    def test_create_book_without_authentication(self):
        self.client.logout()  # Log out to simulate an unauthenticated user
        response = self.client.post('/api/books/', self.book_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test updating a book
    def test_update_book(self):
        update_data = {"title": "Updated Book"}
        response = self.client.put(f'/api/books/{self.book.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], update_data['title'])

    # Test updating a book without authentication
    def test_update_book_without_authentication(self):
        self.client.logout()
        update_data = {"title": "Unauthorized Update"}
        response = self.client.put(f'/api/books/{self.book.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test deleting a book
    def test_delete_book(self):
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    # Test deleting a book without authentication
    def test_delete_book_without_authentication(self):
        self.client.logout()
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)