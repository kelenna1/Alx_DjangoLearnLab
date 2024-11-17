from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

groups_permissions = {
    "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
    "Editors": ["can_view", "can_edit"],
    "Viewers": ["can_view"],
}

content_type = ContentType.objects.get_for_model(Book)
for group_name, perms in groups_permissions.items():
    group, created = Group.objects.get_or_create(name=group_name)
    for perm_codename in perms:
        permission = Permission.objects.get(
            codename = perm_codename,
            content_type = content_type
        )
        group.permissions.add(permission)