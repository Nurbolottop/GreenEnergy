from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import translation
from django.conf import settings
import json

from apps.cms.models import ConnectionRequest, Notification


def landing_view(request):
    if request.method == 'POST':
        org_name = request.POST.get('org_name', '').strip()
        contact_name = request.POST.get('contact_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        comment = request.POST.get('comment', '').strip()

        if org_name and contact_name and phone and email:
            conn_req = ConnectionRequest.objects.create(
                organization_name=org_name,
                contact_name=contact_name,
                phone=phone,
                email=email,
                comment=comment
            )

            Notification.objects.create(
                title='Новая заявка',
                message=f'Заявка на подключение от "{org_name}". Контакт: {contact_name}, {phone}',
                level='info'
            )
            messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('landing')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')

    return render(request, 'include/homepage.html')


def login_view(request):
    """
    Единая страница входа.
    Определяет роль через UserProfile.role и перенаправляет в нужный кабинет.
    """
    if request.user.is_authenticated:
        # Определяем роль через profile
        if _is_platform_admin(request.user):
            return redirect('/platform/dashboard/')
        return redirect('/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            messages.error(request, 'Введите username и password.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, 'Аккаунт отключён. Обратитесь к администратору платформы.')
                return render(request, 'login.html')

            # Проверка статуса профиля и организации
            profile = getattr(user, 'profile', None)
            if profile:
                if profile.status != 'active':
                    messages.error(request, 'Аккаунт отключён. Обратитесь к администратору платформы.')
                    return render(request, 'login.html')

                if profile.is_org_user and profile.organization:
                    if profile.organization.status != 'active':
                        messages.error(request, 'Организация отключена. Обратитесь к администратору платформы.')
                        return render(request, 'login.html')

            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)

            if _is_platform_admin(user):
                return redirect('/platform/dashboard/')
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Неверный username или password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('landing')


def _is_platform_admin(user):
    """Проверяет, является ли пользователь администратором платформы."""
    if user.is_superuser or user.is_staff:
        return True
    profile = getattr(user, 'profile', None)
    if profile and profile.role == 'platform_admin':
        return True
    return False


def set_language_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lang_code = data.get('language')
        except Exception:
            lang_code = request.POST.get('language')

        allowed_langs = [lang[0] for lang in getattr(settings, 'LANGUAGES', [])] if hasattr(settings, 'LANGUAGES') else ['ru', 'en', 'ky']

        if lang_code in allowed_langs:
            translation.activate(lang_code)
            if hasattr(request, 'session'):
                request.session[translation.LANGUAGE_SESSION_KEY] = lang_code

            response = JsonResponse({'success': True, 'language': lang_code, 'reload': True})
            cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
            response.set_cookie(
                cookie_name,
                lang_code,
                max_age=365 * 24 * 60 * 60,
                domain=getattr(settings, 'SESSION_COOKIE_DOMAIN', None),
                secure=getattr(settings, 'SESSION_COOKIE_SECURE', False),
            )
            return response
    return JsonResponse({'success': False, 'error': 'Invalid request'})
