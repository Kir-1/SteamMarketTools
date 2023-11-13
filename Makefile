up:
	docker-compose -f docker-compose.yaml up -d
build:
	docker-compose -f docker-compose.yaml up -d --build
down:
	docker-compose down

up-dev:
	docker-compose -f docker-compose-dev.yaml up -d

build-dev:
	docker-compose -f docker-compose-dev.yaml up -d --build