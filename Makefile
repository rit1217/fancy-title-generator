.PHONY: install
install:
	python3 -m venv . \
		&& source ./bin/activate \
		&& pip3 install -r requirements.txt \
		&& deactivate \
		&& npm install \


.PHONY: build
build:
	npm run build


.PHONY: run
run:
	source ./bin/activate \
		&& python3 -m api \


.PHONY: clean
clean:
	rm -rf bin include lib lib64 pyvenv.cfg