from django.urls import path
from .views import BookListView,BookDetailView,BookCreateView,BookUpdateView,BookDeleteView

urlpatterns = [
    path('books/', BookListView.as_view(), name='List'),
    path('<int:pk>/books/', BookDetailView.as_view(), name='Detail'),
    path('books/create/', BookCreateView.as_view(), name='Create'),
    path('<int:pk>/books/update/', BookUpdateView.as_view(), name='Update'),
    path('<int:pk>/books/delete/', BookDeleteView.as_view(), name='Delete'),
]
