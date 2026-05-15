from django.contrib import admin
from .models import Organization, UserProfile, Notification, ConnectionRequest, Tariff, Device, EnergyReading


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'period', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured')
    search_fields = ('name', 'description')


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


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'device_id', 'name', 'organization', 'device_type',
        'status', 'is_online', 'relay_status',
        'power', 'voltage', 'current', 'energy',
        'last_seen', 'updated_at',
    )
    list_filter = ('status', 'device_type', 'is_online', 'relay_status', 'organization')
    search_fields = ('device_id', 'name', 'organization__name', 'object_name', 'zone_name')
    readonly_fields = ('created_at', 'updated_at', 'last_seen')


@admin.register(EnergyReading)
class EnergyReadingAdmin(admin.ModelAdmin):
    list_display = ('device', 'voltage', 'current', 'power', 'energy', 'relay_status', 'created_at')
    list_filter = ('relay_status', 'created_at', 'device')
    search_fields = ('device__device_id', 'device__name')
    readonly_fields = ('created_at',)
