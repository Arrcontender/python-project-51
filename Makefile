build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

test:
	poetry run pytest --cov

lint:
	poetry run flake8 page_loader_project

coverage:
	poetry run pytest --cov=page_loader page_loader_project/tests/ --cov-report xml

test-coverage:
	poetry run pytest --cov=. --cov-report xml