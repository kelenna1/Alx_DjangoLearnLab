# Delete the Book instance
retrieved_book.delete()

# Confirm deletion
Book.objects.all()
# Output: <QuerySet []>
