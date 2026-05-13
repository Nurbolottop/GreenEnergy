from django.contrib import admin
from .models import Organization, UserProfile, Notification, ConnectionRequest


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'contract_number', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'contact_person', 'phone', 'email', 'contract_number')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'organization', 'status', 'created_at')
    list_filter = ('role', 'status')
    search_fields = ('user__username', 'organization__name')
    raw_id_fields = ('user', 'organization')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'organization', 'is_read', 'created_at')
    list_filter = ('level', 'is_read')
    search_fields = ('title', 'message')


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'contact_name', 'phone', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('organization_name', 'contact_name', 'phone', 'email')
