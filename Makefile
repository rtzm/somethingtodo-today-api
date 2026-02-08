PHONY: run

run:
	docker compose up -d --build
	sleep 3
	uv run -- fastapi dev main.py