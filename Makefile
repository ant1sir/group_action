all: distro upload

distro:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload --skip-existing dist/*

