import flask
import api.trie_model as trie_model

def read_data():
    try:
        data_file = open('./temp/data/pre_proceed_data.txt', 'r')
    except:
        trie_model.data_preprocess()
        data_file = open('./temp/data/pre_proceed_data.txt', 'r')

    content = data_file.read().splitlines()
    data_file.close()
    data_list = []
    for line in content:
        data_list.append(line)

    return data_list


app = flask.Flask(__name__)

data = read_data()

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
