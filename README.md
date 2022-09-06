# Setup 

## ***.env*** file

Create ***.env*** file with variables like in ***.env.example*** with using your own data:

```
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=db_host
DB_PORT=db_port
SU_NAME=test_name
SU_PASSWORD=test_password
DEBUG=1
```

## Docker

```shell
docker compose build
docker compose up
```

## Without docker

### 1. Postgres

>Create user

>Create DB

### 2. Venv

```shell
python -m venv venv
```

and use them

### 3. Requirements

```shell
pip install -r requirements.txt
```

### 4. Migrations

```shell
python manage.py migrate
```
### 5. Superuser

```shell
python manage.py createsuperuser
```

### 6. Start server

```shell
python manage.py runserver
```
