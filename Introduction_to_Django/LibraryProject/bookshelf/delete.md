# Delete the Book instance
from bookshelf.models import Book
retrieved_book.delete()

# Confirm deletion
Book.objects.all()
# Output: <QuerySet []>
