#!/bin/bash
# Скрипт для запуска миграции и создания суперпользователя

python ./manage.py migrate
python ./manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@mail.com', 'admin')"