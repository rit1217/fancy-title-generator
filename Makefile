.PHONY: install
install:
	python3 -m venv . \
		&& source ./bin/activate \
		&& pip3 install -r requirements.txt \
		&& deactivate \


.PHONY: run
run:
	source ./bin/activate \
		&& python3 -m api \


.PHONY: clean
clean:
	rm -rf bin include lib lib64 pyvenv.cfg