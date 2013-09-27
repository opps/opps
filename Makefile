
.PHONY: test
test: pep8
	coverage run runtests.py

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
	@flake8 opps --ignore=F403,F401 --exclude=migrations

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
	@sh scripts/compilemessages.sh

.PHONY: tx
tx:
	@sh scripts/tx.sh

.PHONY: txpush
txpush:
	tx push --source --translations

.PHONY: txpull
txpull:
	tx pull -a
