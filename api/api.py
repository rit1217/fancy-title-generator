import flask

import api.trie_model as trie_model

app = flask.Flask(__name__,
                 static_url_path='',
                 static_folder='../build',
                 template_folder='../build')

data = trie_model.data_preprocess()

trie = trie_model.Trie()
trie.add_data(data)

@app.route('/')
def index():
    return flask.render_template("index.html")  

@app.route('/api/autocomplete/', methods = ['POST'])
def suggest_complete():
    req_body = flask.request.get_json()
    res = trie.autocomplete(req_body['prefix'], 20)
    return flask.jsonify(res)
