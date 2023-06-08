run: build
	docker compose down
	docker compose up

install:
	git submodule init
	git submodule update --init --recursive --jobs 8

build: install
	docker build -t bifrost:latest ./Bifrost
	docker build -t bifrost:cFS .

login: build
	docker compose run -it bifrost bash || true
