
.PHONY: test
test: pep8
	python runtests.py

.PHONY: travis
travis:
	pip install -r requirements_dev.txt --use-mirrors
	export OPPS_TRAVIS=True
	python setup.py develop

.PHONY: install
install:
	python setup.py develop

.PHONY: pep8
pep8:
	@flake8 opps --ignore=F403 --exclude=migrations

.PHONY: sdist
sdist: test
	@python setup.py sdist upload

.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;

.PHONY: makemessages
makemessages:
	@sh scripts/makemassages.sh

.PHONY: compilemessages
compilemessages:
	for api archives articles bin boxes channels containers contrib core db flatpages images search sitemaps sources views; do\
	    echo "make $$resource";\
	    cd opps/$$resource;\
		django-admin.py compilemessages;\
		cd ../../;\
	done

.PHONY: tx
tx:
	for api archives articles bin boxes channels containers contrib core db flatpages images search sitemaps sources views; do\
		tx set --auto-local -r opps-core.$$resource "opps/$$resource/locale/<lang>/LC_MESSAGES/django.po" --source-language=en_US --source-file "opps/$$resource/locale/en_US/LC_MESSAGES/django.po" --execute;\
	done

.PHONY: txpush
txpush:
	tx push --source --translations

.PHONY: txpull
txpull:
	tx pull -a
