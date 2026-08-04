install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

build:
	bash ./build.sh

start:
	rm -f db.sqlite3
	uv run python manage.py migrate
	uv run python manage.py runserver

render-start:
	uv run gunicorn task_manager.wsgi:application --bind 0.0.0.0:$(PORT)

test:
	uv run python manage.py test
