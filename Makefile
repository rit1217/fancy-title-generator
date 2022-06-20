CONTAINER := ml-similar-items-item2vec-model-training
VERSION := "src/__init__.py:__version__"

.PHONY: local/install
local/install:
	python3 -m venv . \
		&& source ./bin/activate \
		&& pip3 install -r requirements.txt \
		&& deactivate \
		&& npm install \

.PHONY: local/run/server
local/run/server:
	source ./bin/activate \
		&& python3 -m fancy_title_generator \

.PHONY: local/run/web
local/run/web:
	npm start 

.PHONY: local/clean
local/clean:
	rm -rf bin include lib lib64 pyvenv.cfg