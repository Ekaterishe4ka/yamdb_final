![Yamdb Workflow Status](https://github.com/Ekaterishe4ka/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

# Описание

Учебный проект 16 спринта курса Python-разработчик в Яндекс.Практикум

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В этом спринте мы работали с облачным сервисом GitHub Actions.

# Стек технологий

- Python
- Django
- Docker
- Nginx

## Описание Workflow
### Workflow состоит из четырёх шагов:
#### tests
- Проверка кода на соответствие PEP8, автоматический запуск тестов.
#### Push Docker image to Docker Hub
- Сборка и публикация образа на DockerHub.
#### deploy 
- Автоматический деплой на боевой сервер при пуше в главную ветку main.
#### send_massage
- Отправка уведомления в телеграм-чат.


# Установка

Клонировать репозиторий на локальную машину:

```
https://github.com/Ekaterishe4ka/yamdb_final.git
```

Установка на удаленном сервере (Ubuntu):
Прежде, чем приступать к работе, необходимо выполнить вход на свой удаленный сервер:

```
ssh <USERNAME>@<IP_ADDRESS>
```

Установите docker на сервер:

```
sudo apt install docker.io
```

Установите docker-compose на сервер:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Скопируйте подготовленные файлы:
`docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf` соответственно.
Введите команду из корневой папки проекта:

```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp -r nginx/ <username>@<host>:/home/<username>/
```

Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

```

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```

После успешного деплоя:
Зайдите на боевой сервер и выполните команды:

```
sudo docker-compose exec web python manage.py makemigrations --noinput # Создаем и применяем миграции
sudo docker-compose exec web python manage.py migrate --noinput
```

```
sudo docker-compose exec web python manage.py collectstatic --no-input # Подгружаем статику
```

```
sudo docker-compose exec web python manage.py loaddata fixtures.json # Заполняем базу данными
```

Создать суперпользователя Django:

```
sudo docker-compose exec web python manage.py createsuperuser
```


## Проект будет доступен по вашему IP-адресу.

Образ на DockerHub: https://hub.docker.com/repository/docker/katerina23/yamdb

# Автор проекта

Екатерина Богомолова
