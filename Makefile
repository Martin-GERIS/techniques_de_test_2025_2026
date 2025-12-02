test:
	pytest -v

unit_test:
	pytest -v Triangulator/Tests/test_unit.py
	pytest -v Triangulator/Tests/test_integration.py

perf_test:
	pytest -v Triangulator/Tests/test_perf.py

coverage:
	coverage run -m pytest
	coverage html
	coverage report

coverage_report:
	coverage html
	coverage report

lint:
	ruff check .

doc:
	pdoc3 --html --output-dir docs App