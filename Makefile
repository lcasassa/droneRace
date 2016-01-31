PROJECT_NAME=DroneRace
PROJECT_PATH=droneRace
DOCPATH=$(PROJECT_PATH)/doc/
BRANCH=$(shell git rev-parse --abbrev-ref HEAD)
FEATURE=$(shell echo $(BRANCH) | cut -d / -f 2)

all:
	python setup.py bdist_wheel

test:
	nosetests --with-coverage --cover-branches --cover-erase --cover-package=$(PROJECT_PATH)

uninstall:
	pip uninstall -y $(PROJECT_NAME) || echo "$(PROJECT_NAME) already uninstalled."

install-develop: clean uninstall
	python setup.py develop

install: clean uninstall all
	pip install dist/$(PROJECT_NAME)-2.0.0-py2-none-any.whl

clean:
	echo "Deleting all *.c *.cpp *.pyc *.so in ./$(PROJECT_PATH)/"
	find $(PROJECT_PATH)/ -iname "*.c" -exec rm '{}' \;
	find $(PROJECT_PATH)/ -iname "*.cpp" -exec rm '{}' \;
	find $(PROJECT_PATH)/ -iname "*.pyc" -exec rm '{}' \;
	find $(PROJECT_PATH)/ -iname "*.so" -exec rm '{}' \;
	echo "Deleting build dist $(PROJECT_PATH).egg-info"
	rm -rf build dist $(PROJECT_PATH).egg-info

pylint:
	pylint --disable=R0401,R0903,R0902,locally-disabled,abstract-class-little-used -f parseable $(PROJECT_PATH)/

setenv:
	virtualenv env
	( . env/bin/activate; pip install -r requirements --upgrade )

install-opencv:
	sudo apt-get install python-opencv

cleanenv:
	rm -rf env

doc: cleandoc
	# Generating documentation for packages...
	cd $(DOCPATH)
	sphinx-build $(DOCPATH) $(DOCPATH)_build/

cleandoc:
	rm -Rf $(DOCPATH)_build/

