from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [ 'title', 'publication_year']
    def validate_publication_year(self, date):
        if date > date.today():
            raise serializers.ValidationError('The Publication date cannot be in the future.')
        return date
class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name']