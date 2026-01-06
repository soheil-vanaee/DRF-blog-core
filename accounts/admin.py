from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'account_creation_date')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'account_creation_date', 'last_login_date')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-account_creation_date',)

    # Define fieldsets for the user form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'ip_address')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login_date', 'account_creation_date')}),
    )

    # Define add_fieldsets for creating new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Read-only fields (these can't be edited)
    readonly_fields = ('account_creation_date', 'last_login_date')


# Register the custom user model with the admin
admin.site.register(CustomUser, CustomUserAdmin)
