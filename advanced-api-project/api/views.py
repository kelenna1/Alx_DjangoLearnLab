from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Book
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAuthenticated
from django_filters import rest_framework
from rest_framework import filters
from rest_framework import generics
from .serializers import BookSerializer
from .filters import BookFilter

# Create your views here.
class BookListView(IsAuthenticatedOrReadOnly,ListView):
    model = Book
    template_name = 'List.html'
    context_object_name = 'books'
    
class BookDetailView(IsAuthenticatedOrReadOnly,DetailView):
    model = Book
    template_name = 'Detail.html'
    context_object_name = 'book'
    
class BookCreateView(IsAuthenticated,CreateView):
    model = Book
    template_name = 'Form.html'
    fields = ['title', 'publication_year', 'author']
    success_url = reverse_lazy('List')

class BookUpdateView(IsAuthenticated,UpdateView):
    model = Book
    template_name = 'Form.html'
    fields = ['title', 'publication_year', 'author']
    success_url = reverse_lazy('List')
    
class BookDeleteView(IsAuthenticated,DeleteView):
    model = Book
    template_name = 'Delete.html'
    success_url = reverse_lazy('List')
    
class BookListApiView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    order = filters.OrderingFilter
    search = filters.SearchFilter
    
    filterset_class = BookFilter
    search_fields = ['title', 'author']
    ordering_fields =['title', 'publication_year']
    ordering = ['title']