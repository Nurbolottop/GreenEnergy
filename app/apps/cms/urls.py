from django.urls import path
from . import views

urlpatterns = [
    # Platform Admin
    path('platform/dashboard/', views.platform_dashboard_view, name='platform_dashboard'),
    path('platform/organizations/', views.platform_organizations_view, name='platform_organizations'),
    path('platform/organizations/create/', views.platform_organization_create_view, name='platform_organization_create'),
    path('platform/organizations/<int:org_id>/', views.platform_organization_detail_view, name='platform_organization_detail'),
    path('platform/notifications/', views.platform_notifications_view, name='platform_notifications'),
    path('platform/notifications/<int:notif_id>/read/', views.platform_notification_read_view, name='platform_notification_read'),
    path('platform/notifications/read-all/', views.platform_notifications_read_all_view, name='platform_notifications_read_all'),
    path('platform/requests/', views.platform_requests_view, name='platform_requests'),
    path('platform/requests/<int:req_id>/', views.platform_request_update_view, name='platform_request_update'),
    path('platform/settings/', views.platform_settings_view, name='platform_settings'),
    path('platform/settings/tariff/save/', views.platform_tariff_save_view, name='platform_tariff_save'),
    path('platform/settings/tariff/<int:tariff_id>/delete/', views.platform_tariff_delete_view, name='platform_tariff_delete'),
    path('api/devices/data/', views.device_data_api, name='device_data_api'),
    path('platform/api/devices/<int:device_id>/status/', views.device_status_api, name='device_status_api'),

    # Organization User
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('devices/', views.devices_view, name='devices'),
    path('devices/<int:device_id>/', views.device_detail_view, name='device_detail'),
    path('monitoring/', views.monitoring_view, name='monitoring'),
    path('alerts/', views.alerts_view, name='alerts'),
]
