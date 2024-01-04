# Благотворительный фонд QRKot

## О проекте

QRКот - приложение для Благотворительного фонда поддержки котиков QRKot.

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

Также существует возможность формирования отчёта в гугл-таблице, где представлены закрытые проекты, отсортированные по скорости сбора средств: от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

## Технологии
- Alembic 1.7.7
- FastAPI 0.78.0
- Python 3.10.5
- Pydantic 1.9.1
- SQLAlchemy 1.4.36

## Как заполнить файл .env
- DATABASE_URL = <> #Выбор базы данных (по умолчанию: sqlite+aiosqlite:///./fastapi.db)
- SECRET = <> #Секретный ключ (пример: qwerty)
### Далее идут данные из JSON-файла с данными сервисного аккаунта Google Cloud Platform
- TYPE = <...>
- PROJECT_ID = <...>
- PRIVATE_KEY_ID = <...>
- PRIVATE_KEY = <...>
- CLIENT_EMAIL = <...>
- CLIENT_ID = <...>
- AUTH_URI = <...>
- TOKEN_URI = <...>
- AUTH_PROVIDER_X509_CERT_URL = <...>
- CLIENT_X509_CERT_URL = <...>
- UNIVERSE_DOMAIN = <...>
- EMAIL = <...> #Почта, на которую будет выдан доступ к созданным гугл-таблицам

## Документация к API
- [docs](http://127.0.0.1:8000/docs)
- [redoc](http://127.0.0.1:8000/redoc)

## Как запустить проект
Загрузите проект в выбранную директорию:
```
git clone git@github.com:OlegPrizov/QRkot_spreadsheets.git
```

Перейдите в загруженную директорию
```
cd QRkot_spreadsheets
```

Создайте и активируйте виртуальное окружение, обновите pip:
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
```

Установите зависимости:
```
pip install -r requirements.txt
```

Создайте базу данных:
```
alembic upgrade head
```

Запустите проект:
```
uvicorn app.main:app
```
## Автор
- [Олег Призов](https://github.com/OlegPrizov)