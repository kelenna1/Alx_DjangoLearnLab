from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from .forms import ExampleForm

# Create your views here.
permission_required('bookshelf.can_view', raise_exception=True)
def view_book_list(request):
    return HttpResponse("You have permission to view Book.")
permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return HttpResponse("You have permission to craete Book.")
permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return HttpResponse("You have permission to edit Book.")
permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return HttpResponse("You have permission to delete Book.")