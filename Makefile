VERSION := $(shell head -n 1 VERSION)

.PHONY: run clean

run:
	python3 main.py -i input/Sample.txt

docker-build:
   docker build . -t mazegame:latest

docker-run:
    docker run -v $HOME/mnt\:/src/mnt -it mazegame:latest /bin/bash

clean:
	rm -rf tmp/