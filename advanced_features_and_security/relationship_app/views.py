from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

# Create your views here.
def database_books(request):
    book = Book.objects.all()
    context = {
        'books' : Book
    }
    return(render, 'relationship_app/list_books.html', context)

class LibraryBooks(DetailView):
    model = Book
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'books'
    def library_name(self):
        library = self.kwargs['library_name']
        return Book.objects.filter(library_name='library_name')
    def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})
    

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book_view(request):
    return render(request, 'add_book.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def change_book_view(request):
    return render(request, 'change_book.html')

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book_view(request):
    return render(request, 'delete_book.html')


            
