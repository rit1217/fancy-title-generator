.PHONY: install
install:
	python3 -m venv . \
		&& source ./bin/activate \
		&& pip3 install -r requirements.txt \
		&& deactivate \
		&& npm install \

.PHONY: run/api
run/api:
	source ./bin/activate \
		&& python3 -m api \

.PHONY: run/web
run/web:
	npm start 

.PHONY: clean
clean:
	rm -rf bin include lib lib64 pyvenv.cfg