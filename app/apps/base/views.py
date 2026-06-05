from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import translation
from django.conf import settings
import json
import random

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

            # Шаг 1 пройден. Логин не выполняем — сначала проверка «вы не робот» (шаг 2).
            request.session['pending_user_id'] = user.id
            request.session['pending_remember'] = bool(remember_me)
            _generate_human_challenge(request)
            return redirect('verify_human')
        else:
            messages.error(request, 'Неверный username или password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def _generate_human_challenge(request):
    """Генерирует простую арифметическую капчу и сохраняет ответ в сессии."""
    a, b = random.randint(1, 9), random.randint(1, 9)
    request.session['human_a'] = a
    request.session['human_b'] = b


def verify_human_view(request):
    """Шаг 2 входа: подтверждение «вы не робот» (галочка + пример)."""
    pending_id = request.session.get('pending_user_id')
    if not pending_id:
        return redirect('login')

    if request.method == 'POST':
        not_robot = request.POST.get('not_robot')
        try:
            answer = int(request.POST.get('captcha_answer', ''))
        except (ValueError, TypeError):
            answer = None

        correct = request.session.get('human_a', 0) + request.session.get('human_b', 0)

        if not not_robot:
            messages.error(request, 'Отметьте «Я не робот», чтобы продолжить.')
            _generate_human_challenge(request)
        elif answer != correct:
            messages.error(request, 'Неверный ответ на проверку. Попробуйте ещё раз.')
            _generate_human_challenge(request)
        else:
            user = User.objects.filter(id=pending_id).first()
            if not user or not user.is_active:
                _clear_pending(request)
                messages.error(request, 'Сессия истекла. Войдите заново.')
                return redirect('login')

            remember = request.session.get('pending_remember', False)
            _clear_pending(request)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if not remember:
                request.session.set_expiry(0)

            if _is_platform_admin(user):
                return redirect('/platform/dashboard/')
            return redirect('/dashboard/')

    if 'human_a' not in request.session:
        _generate_human_challenge(request)

    context = {
        'a': request.session.get('human_a'),
        'b': request.session.get('human_b'),
    }
    return render(request, 'verify_human.html', context)


def _clear_pending(request):
    for key in ('pending_user_id', 'pending_remember', 'human_a', 'human_b'):
        request.session.pop(key, None)


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
