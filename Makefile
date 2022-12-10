test:
	cd dosuri/user && pytest
	cd dosuri/hospital && pytest
	python3 manage.py test --settings=config.settings_test