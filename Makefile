up:
	docker-compose up -d api && make log

log:
	docker-compose logs -f

down:
	docker-compose down