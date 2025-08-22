# DJANGO_COURSE_PROJ
## Описание
Данный проект - это реализация проекта **Проект 5. Трекер привычек** от *SkyPro*.
  
## Инструкция по установке  
Для того, чтобы проверить код из данного репозитория вам понадобятся **Python**, **Poetry** и **Pycharm**, так что перед началом убедитесь, что они установлены на ваш ПК (проект пишется на версии Python 3.12.7).
Если хотите использовать Python версии ниже, чем 3.12, необходимо отредактировать файл **pyproject.toml**.  
Найдите в нем строчки и вместо **3.12** впишите версию Python, которую хотите использовать:  
```
[tool.poetry.dependencies]  
python = "^3.12"  
```

После чего скачайте все файлы проекта одним архивом:  
```
<> Code -> Download ZIP  
```

Разархивируйте скачанный файл в любое удобное для Вас место.  
Откройте папку проекта **DRF_COURSE_PROJECT** с помощью **PyCharm**. 

Для работы приложения пропишите в терминале
~~~
poetry install
~~~
## Инструкция по использованию
Запустите в терминале
~~~
python manage.py runserver
~~~

В **POSTMAN** можно проверить работу контроллеров. **URLS** можете найти в проекте, в папке **config, users и habits**

## Инструкция Docker
**Запуск приложения**

Для запуска всех сервисов, определенных в файле 
docker-compose.yml
, используйте команду:

~~~
docker-compose up -d --build
~~~

**Рассмотрим основные команды управления Docker Compose:**
~~~
docker-compose up
~~~
 — запускает все сервисы, определенные в файле 
docker-compose.yml
. Если образы для сервисов еще не созданы, они будут собраны перед запуском.
Флаг 
-d
 позволяет запустить контейнеры в фоновом режиме (Detach):
~~~
docker-compose up -d
~~~
~~~
docker-compose down
~~~
 — останавливает все работающие контейнеры и удаляет контейнеры, сети, тома и образы, созданные командой 
docker-compose up
.
~~~
docker-compose build
~~~
 — собирает образы для всех сервисов, используя Dockerfile, определенный в конфигурации.
~~~
docker-compose logs
~~~
 — позволяет просматривать логи всех контейнеров. Это полезно для отладки и мониторинга работы контейнеров.
~~~
docker-compose ps
~~~
 — выводит список всех контейнеров, созданных Docker Compose, и их текущее состояние.
~~~
docker-compose exec
~~~
 — позволяет выполнять команды внутри работающего контейнера. Это полезно для выполнения административных задач или отладки.
docker-compose exec service_name command
Где:

service_name
 — это имя контейнера, которое можно узнать с помощью команды 
docker ps
.
 
command
 — команда, которую нужно выполнить внутри контейнера.
Пример выполнения команды 
bash
 внутри контейнера 
web
:

docker-compose exec web bash

**Остановка и удаление контейнеров**

Чтобы остановить все работающие контейнеры и удалить контейнеры, сети, тома и образы, созданные командой 
docker-compose up
, используйте команду:

~~~
docker-compose down
~~~

**Просмотр логов**

Для просмотра логов всех контейнеров используйте команду:

~~~
docker-compose logs
~~~

## Настройка для виртуальной машины

Подключитесь к виртуальной машине с помощью команды, отображаемой в вашей личном кабинете yandex cloud:

~~~
ssh -l your_VM_login your_VM_public_IP
~~~

Обновите систему и установите Docker:

~~~
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
~~~

Добавьте пользователя в группу docker:

~~~
sudo usermod -aG docker $USER
newgrp docker
~~~

Создайте директорию для проекта и перейдите в нее:
~~~
mkdir -p ~/DRF_course_project
cd ~/DRF_course_project
~~~

**!!! НЕ ЗАКРЫВАЙТЕ ТЕРМИНАЛ, ОН ПОНАДОБИТСЯ ЧУТЬ ПОЗЖЕ !!!**

Перейдите в вашем репозитории GitHub в Settings → Secrets and variables → Actions. Добавьте следующие secrets:

| First Header  | Second Header                            |
| ------------- |------------------------------------------|
| SSH_KEY  | Приватный SSH ключ для доступа к серверу |
| SSH_USER  | SSH пользователь (например: ubuntu)      |
| SERVER_IP  | IP адрес вашего сервера                  |
| SECRET_KEY  | Django SECRET_KEY                        |
| DEBUG  | Django DEBUG (False для production)      |
| DOCKER_HUB_ACCESS_TOKEN  | Docker Hub Access Token                  |
| DOCKER_HUB_USERNAME  | Docker Hub username                      |
| BOT_TOKEN  | Токен телеграм бота                      |

Создайте репозиторий на Docker Hub
Сгенерируйте Access Token:
- Зайдите в Docker Hub → Account Settings → Security → New Access Token
- Сохраните токен в GitHub Secrets как DOCKER_HUB_ACCESS_TOKEN

Сделайте fork проекта в свой github и клонируйте проект на сервер в папку DRF_course_project и к себе локально на компьютер (сделайте это из терминала открытом на первых шагах, вы должны находиться в папке **DRF_course_project**:

~~~
git clone git@github.com:your-username/DRF_COURSE_PROJECT.git -b your_branch
git pull
~~~

Закоммитьте изменения в вашу ветку:

~~~
git add .
git commit -m "Deploy preparation"
git push origin your_branch
~~~

GitHub Actions автоматически запустит workflow:
- Сборка Docker образа
- Запуск тестов
- Пуш образа в Docker Hub
- Деплой на сервер

Проверьте работу приложения. Перейдите по публичному ip вашего сервера в браузере, вы должны увидеть:

~~~
Page not found (404)

Using the URLconf defined in config.urls, Django tried these URL patterns, in this order:

1. admin/
2. habits/
3. users/
4. swagger/ [name='schema-swagger-ui']
5. redoc/ [name='schema-redoc']

You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.
~~~

