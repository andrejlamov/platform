MONGO := mongodb-linux-x86_64-3.2.6
CONDA := Miniconda3-latest-Linux-x86_64

export LC_ALL=C

# shortcuts
M=$(MONGO)/bin
C=$(CONDA)/bin

export DB_PORT=1336

.PHONY: test

test:  $(M)/mongod $(CONDA) /tmp/mongodb-$(DB_PORT).sock
	mkdir -p test_db log
	$(C)/trial test_api

/tmp/mongodb-$(DB_PORT).sock:
	$(M)/mongod  --fork --logpath log/test_db.log --dbpath test_db --port $(DB_PORT)

## mongo

$(M)/mongod: $(MONGO).tgz $(MONGO)

$(MONGO):
	tar xvf $(MONGO).tgz

$(MONGO).tgz:
	curl -O "https://fastdl.mongodb.org/linux/$(MONGO).tgz"

## python
$(CONDA): $(CONDA).sh $(C)/python
	make packages

$(C)/python:
	sh $(CONDA).sh -b -p $(CONDA)

$(CONDA).sh:
	curl -O https://repo.continuum.io/miniconda/$(CONDA).sh

packages:
	$(C)/conda install -y --file conda.txt
	$(C)/pip install --upgrade pip
	$(C)/pip install -r pip.txt

elpy:
	$(C)/pip install jedi flake8 importmagic autopep8 yapf

clean:
	git clean -fdx
	rm /tmp/mongodb-$(DB_PORT).sock
