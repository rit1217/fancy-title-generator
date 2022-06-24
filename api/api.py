import flask
import graph_model

app = flask.Flask(__name__)

model = graph_model.GraphModel().load()
print(type(model))
@app.route('/')
def index():
    return flask.render_template("index.html")  

@app.route('/api/autocomplete/', methods = ['POST'])
def suggest_complete():
    req_body = flask.request.get_json()
    res = model.predict(req_body['prefix'], 20)
    return flask.jsonify(res)
