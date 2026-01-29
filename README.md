# my_quiz
A quiz platform that allows users to take quizzes, create their own, and share them with others
Ось детальний опис проекту Quiz-платформа (Система тестування). Це чудовий вибір для відновлення знань Django, оскільки він зачіпає складні зв’язки між моделями (Many-to-Many, Foreign Key) та логіку обробки форм.
📝 Основна концепція

Веб-додаток, де адміністратори (або зареєстровані вчителі) створюють тести з питаннями, а користувачі проходять їх, отримують бали та бачать свою статистику.
🛠️ Технічний стек (що можна потренувати)

    Django Models: Зв'язки «Тест -> Питання -> Варіанти відповідей».

    Django Forms / Formsets: Динамічне створення кількох варіантів відповіді.

    Logic: Алгоритм підрахунку правильних відповідей у View.

    Sessions: Щоб користувач не міг просто оновити сторінку і скинути таймер (якщо захочеш його додати).

🗄️ Структура бази даних (Моделі)

    Quiz (Тест):

        Назва, опис, категорія.

        Автор (User).

        Дата створення.

        Складність (Easy, Medium, Hard).

    Question (Питання):

        FK до Quiz.

        Текст питання.

    Answer (Варіант відповіді):

        FK до Question.

        Текст відповіді.

        Boolean-поле is_correct (чи є ця відповідь правильною).

    Result (Результат):

        FK до User.

        FK до Quiz.

        Кількість балів.

        Дата проходження.

🚀 Функціонал по етапах
Етап 1: Базовий (MVP)

    Адмінка Django для створення тестів.

    Головна сторінка зі списком усіх тестів.

    Сторінка проходження: виводиться питання і варіанти (radio buttons).

    Сторінка результату: після натискання "Відправити" показується: "Ви відповіли правильно на 8 з 10 питань".

Етап 2: Просунутий

    Авторизація: Тільки логіновані користувачі можуть проходити тести.

    Особистий кабінет: Історія пройдених тестів та динаміка балів.

    Таймер: На кожен тест дається, наприклад, 5 хвилин.

    Рандомізація: Питання виводяться у випадковому порядку.

Етап 3: "Зірочка" (Full-stack)

    Django Rest Framework (DRF): Зробити API для тестів.

    SPA елементи: Проходження тесту без перезавантаження сторінки (на JavaScript або HTMX).

    Експорт: Можливість завантажити сертифікат про проходження у PDF.


Чудово. Тоді ми можемо планувати production-ready Docker-compose архітектуру для Oracle Cloud Free Tier, де все працює у власних контейнерах.
Твоя мета: Django + Postgres + optional Google OAuth, без Redis/Celery поки що.

Нижче оптимальна структура проєкту:

1. Структура директорій і файлів
my_project/
├── backend/                # твій Django-проєкт
│   ├── Dockerfile          # контейнер для Django
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/             # settings, wsgi, asgi
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── app/                # твій Django apps
│       └── ...
├── docker-compose.yml      # усі контейнери
├── .env                    # локальні/production env variables
├── nginx/
│   ├── Dockerfile          # optional, reverse proxy для SSL
│   └── nginx.conf
└── README.md

2. Dockerfile для Django (backend/Dockerfile)
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

3. Docker-compose (docker-compose.yml)
version: "3.9"

services:
  web:
    build: ./backend
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    volumes:
      - ./backend:/app

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: myproject
      POSTGRES_USER: myproject
      POSTGRES_PASSWORD: supersecret
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

4. .env приклад
DEBUG=False
SECRET_KEY=your-secret-key
POSTGRES_DB=myproject
POSTGRES_USER=myproject
POSTGRES_PASSWORD=supersecret
DATABASE_URL=postgres://myproject:supersecret@db:5432/myproject
ALLOWED_HOSTS=your-oracle-vm-ip-or-domain


Порада: у production краще використовувати домен і SSL через Nginx + Let's Encrypt.

5. Django settings.py (Postgres через env)
import os
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

6. Nginx (optional, для production)

Reverse proxy + HTTPS через Let's Encrypt

Порти 80/443 → проксі до контейнера web

На Oracle Cloud Free Tier можна пробувати SSL через certbot + Nginx

7. Локальний запуск
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

8. Особливості на Oracle Cloud Free Tier

Free VM RAM: 1 GB → нормально для web + Postgres

Потрібно відкрити порт 8000 у firewall (security list) для тестів

Для production → Nginx + 443 порт + Let's Encrypt

Контейнери persistent volumes → Postgres не втратить дані після redeploy

✅ Підсумок

Один проект, docker-compose

Web + Postgres окремі контейнери

Легко додати Redis/Celery пізніше

Google OAuth можна додати без змін Docker

Якщо хочеш, я можу наступним кроком зробити готовий production-ready docker-compose для Oracle VPS з Django, Postgres, Nginx і Let’s Encrypt, щоб ти відразу міг деплоїти.