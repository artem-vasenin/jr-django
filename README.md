# jr-django

rm .env && cp .env_default .env  && docker compose up --build

docker compose down -v

rm .env && cp .env_local .env && python manage.py runserver

http://localhost

