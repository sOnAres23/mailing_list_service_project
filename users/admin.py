from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'phone_number', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'phone_number', 'avatar')}),

        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone_number',
                       'avatar', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'username',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
