import flask
import flask_cors

import api.trie_model as trie_model

app = flask.Flask(__name__)
flask_cors.CORS(app)

api_v1 = flask.Blueprint('api_v1', __name__, url_prefix='/api/v1')

data = trie_model.data_preprocess()

trie = trie_model.Trie()
trie.add_data(data)

@api_v1.route('/nextword/', methods = ['POST'])
def suggest_next_word():
    req_body = flask.request.get_json()
    res = trie.get_next_char(req_body['prefix'])[:20]
    return flask.jsonify(res[:20])
  

@api_v1.route('/complete/', methods = ['POST'])
def suggest_complete():
    req_body = flask.request.get_json()
    res = trie.autocomplete(req_body['prefix'])
    return flask.jsonify(res[:20])

app.register_blueprint(api_v1)
