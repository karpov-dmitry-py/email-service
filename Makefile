.PHONY: .run
.run:
	docker-compose build --no-cache
	docker-compose up -d

.PHONY: .stop
.stop:
	docker-compose stop


.PHONY: .kill
.kill:
	docker-compose rm -f
	docker-compose down


run: .run

stop: .stop

kill: .kill