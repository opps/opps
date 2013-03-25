
.PHONY: test
test: pep8
	DJANGO_SETTINGS_MODULE=dev_settings \
	django-admin.py test core channels sources

.PHONY: travis
travis:
	pip install -r requirements.txt --use-mirrors
	export OPPS_TRAVIS=True
	python setup.py develop 

.PHONY: install
install:
	pip install -r requirements.txt --use-mirrors
	python setup.py develop 

.PHONY: pep8
pep8:
	@flake8 . --ignore=E501,F403,E126,E127,E128,E303
