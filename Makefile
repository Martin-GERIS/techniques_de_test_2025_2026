test:
	pytest -v

unit_test:
	pytest -vv Triangulator/Tests/test_unit.py Triangulator/Tests/test_integration.py

perf_test:
	pytest -vv -s Triangulator/Tests/test_perf.py

coverage:
	coverage run -m pytest Triangulator/Tests/test_unit.py Triangulator/Tests/test_integration.py
	coverage html
	coverage report

coverage_report:
	coverage html
	coverage report

lint:
	ruff check Triangulator/app

doc:
	pdoc3 --html --output-dir docs Triangulator/app