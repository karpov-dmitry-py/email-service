.PHONY: .run
.run:
	docker-compose build --no-cache
	docker-compose up -d


.PHONY: .kill
.kill:
	docker-compose rm -f
	docker-compose down --volumes


run: .run

kill: .kill