import flask
from model_rnn import Model


model = Model().load()


app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("index.html")  


@app.route('/api/autocomplete/', methods = ['POST'])
def api_autocomplete():
    req_body = flask.request.get_json()
    #result: [(title, score)]
    result = model.predict(req_body['prefix'], req_body['top_n'], req_body['max_length'])
    return flask.jsonify([{'title':x[0], 'score':x[1]} for x in result])
