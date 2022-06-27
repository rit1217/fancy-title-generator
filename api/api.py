import flask
from model_graph import Model


model = Model().load()


app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template("index.html")  


@app.route('/api/autocomplete/', methods = ['POST'])
def api_autocomplete():
    req_body = flask.request.get_json()
    res = model.predict(req_body['prefix'], 20)
    return flask.jsonify(res)
