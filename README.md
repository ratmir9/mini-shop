# Mini-shop
## О проекте.
### Небольшой интернет магазин, в котором реализован основной функционал.

### Реализован следующий функционал:
1. Работа с товарами.
2. Работа с корзиной.
3. Работа с заказами.
4. Работа с пользователями.
5. Регистрацмя авторизация по jwt токену. 

## Инструкция по установке и запуску проекта.

1. **Клонируйте репозитории с github.**

2. **Перейдите в директорию с проектом.**
```
cd mini-shop/
```
### Запуск проекта без использования Docker.

1. **Создайте виртуальное окружение.**
```
python3 -m venv venv
```
2. **Активируйте виртуальное окружение.**
```
source venv/bin/activate
```
3. **Установите зависимости.**
```
pip install -r requirements.txt
```
4. **Создайте файл конфигурации (например `env.sh`).**
```
touch env.sh
```
5. **Создайте БД PostgresSQL.**

6. **Заполните файл (`env.sh`) конфигурации.**
```
export DEBUG=1
export SECRET_KEY='' # SECRET KEY DJANGO
export ALLOWED_HOSTS='localhost 127.0.0.1 [::1]'

# DATABASE ENV
export DB_USER='' # имя пользователя бд 
export DB_PASS='' # пароль от бд
export DB_HOST='localhost'
export DB_PORT=5432 
export DB_NAME='' # название бд
```
7. **Активируйте файл конфигурации.**
```
source env.sh
```
8. **Выполните комвнду для применения миграции.**
```
python manage.py migrate
```
9. **Запустите приложение.**
```
python manage.py runserver
```
### Запуск проекта с помощью Docker.
1. **Создайте файлы `.env` и `.env.db` для конфигурирования проекта.**
```
touch .env
touch .env.db
```
2. **Откройте файл `.env` и заполните следующими данными.**
```
DEBUG=1
SECRET_KEY=you_secret_key
ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# env db
DB_ENGINE=django.db.backends.postgresql
DB_USER=fast
DB_PASSWORD=1234QWE 
DB_NAME=shop
DB_HOST=shop_db
DB_PORT=5432
```
3. **Откройте файл `.env.db` и заполните следущими данными.**
```
POSTGRES_USER=fast
POSTGRES_PASSWORD=1234QWE
POSTGRES_DB=shop
```
**Значение параметров для БД в файлах `.env` и `.env.db` должны совпадать.**


4. **Выполните следующую команду для запуска проекта.**
```
sudo docker-compose up -d
```
5. **Выполните следующую команду для применения миграции.**
```
sudo docker exec -it django_shop python manage.py migrate
```
или `make migrate` используя утилиту make

