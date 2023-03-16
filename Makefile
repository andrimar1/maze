VERSION := $(shell head -n 1 VERSION)

.PHONY: run clean

run:
	python3 main.py -i docs/Sample.txt

docker-build:
   docker build . -t mazegame:latest

clean:
	rm -rf tmp/