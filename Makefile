test:
	cd dosuri/user && pytest
	cd dosuri/hospital && pytest
	cd dosuri/community && pytest
	python3 manage.py test --settings=config.settings_test

image:
	docker build . -f docker/Dockerfile -t public.ecr.aws/r0u1w0s6/dosuri:latest --platform=linux/amd64

push:
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/r0u1w0s6
	docker push public.ecr.aws/r0u1w0s6/dosuri

test-db:
	docker volume create pgdata-test
	docker run -d -p 5432:5432 -v pgdata-test:/home/postgres/pgdata -e POSTGRES_PASSWORD=dosuri postgres