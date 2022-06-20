CONTAINER := ml-similar-items-item2vec-model-training
VERSION := "src/__init__.py:__version__"

.PHONY: local/install
local/install:
	python3 -m venv . \
		&& source ./bin/activate \
		&& pip3 install -r requirements.txt \
		&& deactivate \
		&& cd ./web_frontend && echo "Current dir: /web_frontend"\
		&& npm install \
		&& cd ../ && echo "Current dir: /"

.PHONY: local/run/server
local/run/server:
	source ./bin/activate \
		&& cd ./fancy_title_generator && echo "Current dir: /fancy_title_generator"\
		&& uvicorn api:app --host 0.0.0.0 --port 3100 --reload \
		&& deactivate

.PHONY: local/run/web
local/run/web:
	npm start 

.PHONY: local/clean
local/clean:
	rm -rf bin include lib lib64 pyvenv.cfg