
.PHONY: test
test: pep8
	DJANGO_SETTINGS_MODULE=dev_settings \
	django-admin.py test core

.PHONY: install
install:
	pip install -r requirements.txt --use-mirrors
	python setup.py develop 

.PHONY: pep8
pep8:
	@flake8 . --ignore=E501
