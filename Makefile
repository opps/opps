
.PHONY: test
test:
	@echo ""
	@echo ".. RUN TEST OPPS CMS"
	DJANGO_SETTINGS_MODULE=dev_settings \
	django-admin.py test core
	@echo ".."
	@echo "DONE"
	@echo ""

.PHONY: install
install:
	@echo ""
	@echo ".. INSTALL OPPS CMS"
	@echo ".."
	python setup.py develop 
	@echo ".."
	@echo "DONE"
	@echo ""
