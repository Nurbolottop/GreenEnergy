from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    """Организация-клиент платформы Green Energy."""

    STATUS_CHOICES = (
        ('active', 'Активна'),
        ('inactive', 'Неактивна'),
        ('pending', 'Ожидает'),
        ('blocked', 'Заблокирована'),
    )

    name = models.CharField('Название', max_length=255)
    contact_person = models.CharField('Контактное лицо', max_length=255, blank=True, default='')
    phone = models.CharField('Телефон', max_length=50, blank=True, default='')
    email = models.EmailField('Email', blank=True, default='')
    address = models.CharField('Адрес', max_length=255, blank=True, default='')
    contract_number = models.CharField('Номер договора', max_length=100, blank=True, default='')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Профиль пользователя — роль и привязка к организации."""

    ROLE_CHOICES = (
        ('platform_admin', 'Администратор платформы'),
        ('organization_admin', 'Администратор организации'),
        ('organization_user', 'Пользователь организации'),
    )

    STATUS_CHOICES = (
        ('active', 'Активен'),
        ('inactive', 'Неактивен'),
        ('blocked', 'Заблокирован'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    role = models.CharField('Роль', max_length=50, choices=ROLE_CHOICES, default='organization_user')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='Организация',
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user.username} — {self.get_role_display()}'

    @property
    def is_platform_admin(self):
        return self.role == 'platform_admin'

    @property
    def is_org_user(self):
        return self.role in ('organization_admin', 'organization_user')


class Notification(models.Model):
    """Уведомления платформы."""

    LEVEL_CHOICES = (
        ('info', 'Информация'),
        ('success', 'Успех'),
        ('warning', 'Предупреждение'),
        ('danger', 'Критическое'),
    )

    title = models.CharField('Заголовок', max_length=255)
    message = models.TextField('Сообщение')
    level = models.CharField('Уровень', max_length=20, choices=LEVEL_CHOICES, default='info')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Организация',
    )
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.level}] {self.title}'

    @property
    def time_display(self):
        """Человекочитаемое время."""
        from django.utils import timezone
        diff = timezone.now() - self.created_at
        minutes = int(diff.total_seconds() / 60)
        if minutes < 1:
            return 'только что'
        if minutes < 60:
            return f'{minutes} мин назад'
        hours = minutes // 60
        if hours < 24:
            return f'{hours} ч назад'
        days = hours // 24
        return f'{days} дн назад'


class ConnectionRequest(models.Model):
    """Заявки на подключение с лендинга."""

    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('completed', 'Обработана'),
        ('rejected', 'Отклонена'),
    )

    organization_name = models.CharField('Организация', max_length=255)
    contact_name = models.CharField('Имя', max_length=255)
    phone = models.CharField('Телефон', max_length=50)
    email = models.EmailField('Email')
    comment = models.TextField('Комментарий', blank=True, default='')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.organization_name} — {self.contact_name}'

