from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .admin import CustomUserAdmin

# Register your models here.
from .models import Book
"register", "admin.ModelAdmin"
"list_filter", "author", "publication_year"
"search_fields", "title"

class CustomUserAdmin(UserAdmin):
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)