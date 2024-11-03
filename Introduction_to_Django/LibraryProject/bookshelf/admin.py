from django.contrib import admin
from .models import Book
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Fields to display in list view
    list_filter = ('author', 'publication_year')  # Filters for quick navigation
    search_fields = ('title', 'author')  # Searchable fields for fast lookup

admin.site.register(Book, BookAdmin)

