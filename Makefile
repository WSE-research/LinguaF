.PHONY: dist

clean:
	rm -rf build/ dist/ linguaf.egg-info/ __pycache__/ */__pycache__/
	rm -f *.pyc */*.pyc

install:
	python -m build

test:
	pytest

upload:
	twine upload dist/*
