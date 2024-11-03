## Book Model Definition

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

## CRUD Operations

### Create
```python
from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# Output: <Book: 1984 by George Orwell (1949)>


### Retrieve
```python
# Retrieve the Book instance
retrieved_book = Book.objects.get(id=book.id)
retrieved_book
# Output: <Book: 1984 by George Orwell (1949)>


### Update
```python
# Update the book title
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()
retrieved_book
# Output: <Book: Nineteen Eighty-Four by George Orwell (1949)>


### Delete
```python
# Delete the Book instance
retrieved_book.delete()

# Confirm deletion
Book.objects.all()
# Output: <QuerySet []>
