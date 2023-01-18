test:
	cd dosuri/user && pytest
	cd dosuri/hospital && pytest
	cd dosuri/community && pytest
	python3 manage.py test --settings=config.settings_test

test-db:
	docker volume create pgdata-test
	docker run -d -p 5432:5432 -v pgdata-test:/home/postgres/pgdata -e POSTGRES_PASSWORD=dosuri postgres