PHONY: run

start:
	docker compose up -d --build
	sleep 3
	uv run -- fastapi dev main.py

stop:
	docker compose down -v