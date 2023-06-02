run: build
	docker compose down
	docker compose up

build:
	docker build -t bifrost:latest ../Bifrost
	docker build -t bifrost:cFS .

login:
	docker compose run -it bifrost bash || true
