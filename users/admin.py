from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model"""
    
    list_display = ['username', 'email', 'is_admin', 'is_active', 'date_joined']
    list_filter = ['is_admin', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']
    
    # Use default fieldsets for now to avoid errors
    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets
    
    # Add bulk actions
    actions = ['make_admin', 'remove_admin', 'activate_users', 'deactivate_users']
    
    def make_admin(self, request, queryset):
        """Make selected users admin"""
        count = queryset.update(is_admin=True)
        self.message_user(request, f'Successfully made {count} users admin.')
    make_admin.short_description = "Make selected users admin"
    
    def remove_admin(self, request, queryset):
        """Remove admin status from selected users"""
        count = queryset.update(is_admin=False)
        self.message_user(request, f'Successfully removed admin status from {count} users.')
    remove_admin.short_description = "Remove admin status from selected users"
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'Successfully activated {count} users.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'Successfully deactivated {count} users.')
    deactivate_users.short_description = "Deactivate selected users"
