# استفاده از نسخه رسمی پایتون
FROM python:3.11-slim

# کار کردن در پوشه /app
WORKDIR /app

# کپی کردن فایل‌های requirements
COPY requirements.txt .

# نصب کتابخانه‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن همه فایل‌های پروژه
COPY . .

# جمع‌آوری فایل‌های استاتیک (برای Railway)
RUN python manage.py collectstatic --noinput

# پورتی که برنامه روش اجرا میشه
EXPOSE 8000

# اجرا کردن برنامه با daphne
CMD ["daphne", "chatproject.asgi:application", "--port", "8000", "--bind", "0.0.0.0"]
