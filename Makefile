cleanup:
	find . -type d -name __pycache__ -exec rm -r {} \+

run-example:
	python app.py --debug