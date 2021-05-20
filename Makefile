.PHONY: dist

install:
	python -m build

test:
	pytest

clean:
	rm -rf build/ dist/ textstat.egg-info/ __pycache__/ */__pycache__/
	rm -f *.pyc */*.pyc

upload:
	twine upload --repository testpypi dist/*
