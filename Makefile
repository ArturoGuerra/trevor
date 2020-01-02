.PHONY: deps freeze run


freeze:
	pip freeze > requirements.txt

deps:
	pip install -r ./requirements.txt

run:
	python3.8 ./main.py
