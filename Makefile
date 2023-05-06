test:
	cd dosuri/user && pytest --cov
	cd dosuri/hospital && pytest --cov
	cd dosuri/community && pytest --cov
	cd dosuri/common && pytest --cov
	python3 manage.py test --settings=config.settings_test

image:
	docker build . -f docker/Dockerfile -t 024317434110.dkr.ecr.ap-northeast-2.amazonaws.com/dosuri:latest --platform=linux/amd64

push:
	aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 024317434110.dkr.ecr.ap-northeast-2.amazonaws.com
	docker push 024317434110.dkr.ecr.ap-northeast-2.amazonaws.com/dosuri

test-db:
	docker volume create pgdata-test
	docker run -d -p 5432:5432 -v pgdata-test:/home/postgres/pgdata -e POSTGRES_PASSWORD=dosuri postgres