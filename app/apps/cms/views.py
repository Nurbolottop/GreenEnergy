from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from functools import wraps
from .models import Organization, UserProfile, Notification, ConnectionRequest


# ============================================================
# ACCESS DECORATORS
# ============================================================

def _is_platform_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    profile = getattr(user, 'profile', None)
    return profile and profile.role == 'platform_admin'


def platform_admin_required(view_func):
    """Только для Platform Admin."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not _is_platform_admin(request.user):
            return redirect('/dashboard/')
        return view_func(request, *args, **kwargs)
    return wrapper


def organization_user_required(view_func):
    """Только для Organization User."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if _is_platform_admin(request.user):
            return redirect('/platform/dashboard/')
        return view_func(request, *args, **kwargs)
    return wrapper


# ============================================================
# HELPERS
# ============================================================

def create_notification(title, message, level='info', organization=None):
    """Создаёт уведомление в БД."""
    return Notification.objects.create(
        title=title,
        message=message,
        level=level,
        organization=organization,
    )


# ============================================================
# PLATFORM ADMIN VIEWS
# ============================================================

@platform_admin_required
def platform_dashboard_view(request):
    orgs = Organization.objects.all()
    notifications = Notification.objects.all()[:20]
    unread_count = Notification.objects.filter(is_read=False).count()

    context = {
        'stats': {
            'total_organizations': orgs.count(),
            'active_organizations': orgs.filter(status='active').count(),
            'total_devices': 0,
            'online_devices': 0,
            'offline_devices': 0,
            'active_alerts': unread_count,
            'connection_requests': ConnectionRequest.objects.filter(status='new').count(),
            'total_consumption': '—',
        },
        'organizations': orgs,
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'platform/dashboard.html', context)


@platform_admin_required
def platform_organizations_view(request):
    orgs = Organization.objects.all()
    context = {'organizations': orgs}
    return render(request, 'platform/organizations.html', context)


@platform_admin_required
def platform_organization_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        contact_person = request.POST.get('contact_person', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        contract_number = request.POST.get('contract_number', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not name or not username or not password:
            messages.error(request, 'Заполните обязательные поля: название, username, password.')
            return render(request, 'platform/organization_create.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" уже занят.')
            return render(request, 'platform/organization_create.html')

        # 1. Organization
        org = Organization.objects.create(
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            contract_number=contract_number,
            status='active',
        )

        # 2. User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        # 3. UserProfile
        UserProfile.objects.create(
            user=user,
            role='organization_admin',
            organization=org,
            status='active',
        )

        # 4. Уведомление
        create_notification(
            title='Новая организация',
            message=f'Организация "{name}" успешно создана. Логин: {username}',
            level='success',
            organization=org,
        )

        messages.success(request, f'Организация "{name}" создана. Логин: {username}')
        return redirect('platform_organizations')

    return render(request, 'platform/organization_create.html')


@platform_admin_required
def platform_organization_detail_view(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    org_users = UserProfile.objects.filter(organization=org).select_related('user')
    org_notifications = Notification.objects.filter(organization=org)[:10]
    edit_mode = request.GET.get('edit') == '1'

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'update':
            org.name = request.POST.get('name', org.name).strip()
            org.contact_person = request.POST.get('contact_person', '').strip()
            org.phone = request.POST.get('phone', '').strip()
            org.email = request.POST.get('email', '').strip()
            org.address = request.POST.get('address', '').strip()
            org.contract_number = request.POST.get('contract_number', '').strip()
            org.status = request.POST.get('status', org.status)
            org.save()

            create_notification(
                title='Организация обновлена',
                message=f'Данные организации "{org.name}" изменены.',
                level='info',
                organization=org,
            )
            messages.success(request, f'Организация "{org.name}" обновлена.')
            return redirect('platform_organization_detail', org_id=org.id)

        elif action == 'toggle_status':
            org.status = 'inactive' if org.status == 'active' else 'active'
            org.save()
            status_label = 'активирована' if org.status == 'active' else 'отключена'
            create_notification(
                title=f'Организация {status_label}',
                message=f'Организация "{org.name}" {status_label}.',
                level='success' if org.status == 'active' else 'warning',
                organization=org,
            )
            messages.success(request, f'Организация "{org.name}" {status_label}.')
            return redirect('platform_organization_detail', org_id=org.id)

        elif action == 'reset_password':
            new_password = request.POST.get('new_password', '').strip()
            if new_password and org_users.exists():
                admin_profile = org_users.filter(role='organization_admin').first() or org_users.first()
                admin_profile.user.set_password(new_password)
                admin_profile.user.save()
                create_notification(
                    title='Пароль сброшен',
                    message=f'Пароль пользователя "{admin_profile.user.username}" сброшен.',
                    level='info',
                    organization=org,
                )
                messages.success(request, f'Пароль для "{admin_profile.user.username}" сброшен.')
            else:
                messages.error(request, 'Введите новый пароль.')
            return redirect('platform_organization_detail', org_id=org.id)

    context = {
        'org': org,
        'org_users': org_users,
        'notifications': org_notifications,
        'edit_mode': edit_mode,
    }
    return render(request, 'platform/organization_detail.html', context)


@platform_admin_required
def platform_notifications_view(request):
    """Все уведомления платформы."""
    notifications = Notification.objects.all()[:50]
    unread_count = Notification.objects.filter(is_read=False).count()
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'platform/notifications.html', context)


@platform_admin_required
def platform_notification_read_view(request, notif_id):
    """Отметить уведомление как прочитанное."""
    notif = get_object_or_404(Notification, id=notif_id)
    notif.is_read = True
    notif.save()
    return redirect('platform_notifications')


@platform_admin_required
def platform_notifications_read_all_view(request):
    """Отметить все уведомления как прочитанные."""
    Notification.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, 'Все уведомления отмечены как прочитанные.')
    return redirect('platform_notifications')


@platform_admin_required
def platform_requests_view(request):
    """Список всех заявок на подключение."""
    reqs = ConnectionRequest.objects.all()
    context = {'requests': reqs}
    return render(request, 'platform/requests.html', context)


@platform_admin_required
def platform_request_update_view(request, req_id):
    """Просмотр и обновление статуса заявки."""
    req_obj = get_object_or_404(ConnectionRequest, id=req_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(ConnectionRequest.STATUS_CHOICES):
            req_obj.status = new_status
            req_obj.save()
            messages.success(request, f'Статус заявки от "{req_obj.organization_name}" обновлен.')
        return redirect('platform_request_update', req_id=req_obj.id)
        
    context = {'req': req_obj}
    return render(request, 'platform/request_detail.html', context)


# ============================================================
# ORGANIZATION USER VIEWS
# ============================================================

@organization_user_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


@organization_user_required
def devices_view(request):
    return render(request, 'devices.html')


@organization_user_required
def device_detail_view(request, device_id):
    return render(request, 'device_detail.html')


@organization_user_required
def monitoring_view(request):
    return render(request, 'monitoring.html')


@organization_user_required
def alerts_view(request):
    return render(request, 'alerts.html')
