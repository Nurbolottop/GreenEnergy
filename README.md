# Green Energy — B2B SaaS Platform

**Green Energy** — это многопользовательская B2B-платформа для управления энергопотреблением и мониторинга IoT-устройств. Проект построен на базе фреймворка Django с использованием архитектуры multi-tenant, где разделены права глобального администратора (Platform Admin) и пользователей организаций-клиентов (Organization Admin/User).

## 🌟 Основные возможности

* **Multi-tenant архитектура**: Разделение прав доступа. Platform Admin управляет глобальными настройками, организациями и тарифами. Представители организаций имеют изолированные дашборды только для своих объектов и устройств.
* **Управление организациями**: Создание и отключение компаний-клиентов, назначение тарифов, контроль статуса и логинов.
* **Тарифы и ограничения**: Гибкая настройка тарифных планов (лимиты устройств, объектов, пользователей и сроков хранения истории).
* **Заявки на подключение**: Лендинг с контактной формой для сбора заявок от потенциальных клиентов, автоматическое попадание заявок в админ-панель платформы со статусами обработки.
* **Глобальные настройки**: Модуль управления платформой (API ключи, Telegram боты, безопасность, webhook-и и параметры IoT).
* **Уведомления**: Система оповещений (внутрисистемные и Telegram) о важных событиях: превышение лимита мощности, отключение устройств, новые заявки.

## 🛠 Технологический стек

* **Backend**: Python 3, Django
* **База данных**: PostgreSQL (для хранения данных), Redis (для кеширования и очередей)
* **Frontend**: HTML5, Vanilla CSS (BEM / кастомный UI Kit), JavaScript, Django Templates
* **Инфраструктура**: Docker, Docker Compose (изолированные конфигурации для dev и prod)
* **Локализация**: Встроенный механизм Django i18n (русский, английский, кыргызский).

## 📁 Структура проекта

```text
GreenEnergy/
├── app/                  # Основная директория Django приложения
│   ├── apps/             # Модули (base, cms и др.)
│   ├── templates/        # HTML-шаблоны платформы и лендинга
│   └── manage.py         # Точка входа Django
├── docker/               # Файлы Docker (Dev и Prod конфигурации)
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
├── scripts/              # bash-скрипты для инициализации (entrypoint.sh)
├── .env                  # Локальные переменные окружения (настраиваются из .envtest)
└── README.md             # Этот файл
```

## 🚀 Быстрый старт (Разработка)

Проект полностью упакован в Docker. Вам понадобится установленный `docker` и `docker-compose`.

### 1. Настройка окружения

Скопируйте тестовый файл переменных окружения и при необходимости измените доступы к БД, порты и секретные ключи.

```bash
cp .envtest .env
```

Обязательно проверьте файл `.env`. Важные параметры:
* `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — доступы к PostgreSQL.
* `POSTGRES_HOST=db_greenenergy` — **должен совпадать с названием сервиса в docker-compose**.

### 2. Запуск контейнеров

```bash
docker compose -f docker/docker-compose.yml up --build
```

Контейнер `django_web_greenenergy` автоматически:
1. Выполнит миграции базы данных.
2. Соберет статику (`collectstatic`).
3. Запустит dev-сервер Django.

**Доступ по умолчанию:**
* Платформа: [http://127.0.0.1:8084](http://127.0.0.1:8084) (или другой порт, если вы изменили `8084:8082` в docker-compose.yml).
* Админ-панель Django: `/admin/`

### 3. Создание суперпользователя (Platform Admin)

В новой базе данных нужно создать администратора платформы. Откройте новый терминал и выполните:

```bash
docker exec -it django_web_greenenergy python manage.py createsuperuser
```

## 🚢 Запуск в Production

Для продакшн-окружения используется отдельный docker-compose файл, где Django запускается через `gunicorn`.

```bash
docker compose -f docker/docker-compose.prod.yml up --build -d
```

## 💡 Полезные команды (выполняются в работающем контейнере)

Создание миграций после изменения моделей:
```bash
docker exec django_web_greenenergy python manage.py makemigrations
```

Применение миграций:
```bash
docker exec django_web_greenenergy python manage.py migrate
```

Сборка локализаций (обновление .po файлов):
```bash
docker exec django_web_greenenergy python manage.py makemessages -a
docker exec django_web_greenenergy python manage.py compilemessages
```
