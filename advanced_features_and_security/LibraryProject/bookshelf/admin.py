from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .admin import CustomUserAdmin
from django.contrib.auth.models import User, Group

# Register your models here.
from .models import Book
"register", "admin.ModelAdmin"
"list_filter", "author", "publication_year"
"search_fields", "title"

class CustomUserAdmin(UserAdmin):
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)

user = User.objects.get(username='Vorda')
group = Group.objects.get(name='Editors')
user.groups.add(group)
print(f"{user.username} has been added to {group.name} group")