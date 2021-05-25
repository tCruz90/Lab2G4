install: 
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	#python3 -m pytest -vv --cov=hello test_hello.py
	#python3 -m pytest --nbval notebook.ipynb

lint:
	#hadolint Dockerfile #uncomment to explore linting Dockerfiles
	#pylint --disable=R,C hello.py
	
	
	
all: install lint test	
