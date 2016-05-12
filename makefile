init:
	pip install -r requirements.txt

test:
	cd tests
	py.test tests

test-v:
	cd tests
	py.test tests -vs