import time
import psycopg2
from psycopg2 import OperationalError
import subprocess
import os


def wait_for_db():
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    print("Жду базу данных...")

    while True:
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_pass,
                host=db_host,
                port=db_port,
            )
            conn.close()
            print("База доступна!")
            break
        except OperationalError:
            time.sleep(1)


def run(cmd):
    print(f"{cmd}")
    subprocess.run(cmd, shell=False, check=True)


if __name__ == "__main__":
    wait_for_db()

    # миграции
    run(["python", "manage.py", "migrate"])

    # фикстуры
    if os.path.exists("db_fixtures.json"):
        run(["python", "manage.py", "loaddata", "db_fixtures.json"])

    # статика
    run(["python", "manage.py", "collectstatic", "--noinput"])

    print("Запускаю Gunicorn сервер...")
    run([
        "gunicorn",
        "--bind", "0.0.0.0:8000",
        "shop.wsgi:application",
        "--workers", "3"
    ])
