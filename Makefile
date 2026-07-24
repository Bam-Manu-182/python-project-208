install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

build:
	bash ./build.sh

start:
	uv run gunicorn task_manager.wsgi

test:
	uv run python manage.py runserver
