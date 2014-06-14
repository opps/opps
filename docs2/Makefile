.PHONY: github
github:
	@mkdocs build
	@ghp-import site
	@git push origin gh-pages

.PHONY: serve 
serve:
	@mkdocs serve
