.PHONY: install
install:
	python3 -m venv . \
		&& source ./bin/activate \
		&& pip3 install -r requirements.txt \
		&& deactivate


.PHONY: train/trie
train/trie:
	source ./bin/activate \
		&& python3 -m model_graph


.PHONY: train/rnn
train/rnn:
	source ./bin/activate \
		&& python3 -m model_rnn -t


.PHONY: api
api:
	source ./bin/activate \
		&& python3 -m api


.PHONY: clean
clean:
	rm -rf bin include lib lib64 pyvenv.cfg