NAME=macDetec
TEST_PATH=./

.PHONY:   clean build run all
.DEFAULT: all

all: clean build run 

clean:
	rm --force *.pyc
	rm --force *.pyo
	rm --force *.log
	rm --force files/oui.txt
	rm --force files/*.json
	touch debug.log

build:
	python3 $(NAME).py


