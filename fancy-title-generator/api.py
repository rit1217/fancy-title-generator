from fastapi import FastAPI
from pydantic import BaseModel
from graph_approach.trie import Trie
import model.data_prep as data_prep
app = FastAPI()

data2 = data_prep.data2_preparation('../data/fashionData2.csv')
res = data_prep.word_sequence_preparation('../data/fashionProducts.csv')

t = Trie()
t.add_data(res)
t.add_data(data2)

class InputModel(BaseModel):
    input_str: str

@app.post("/nextword/")
def suggest_next_word(prefix: InputModel):
    prepared_in_str = data_prep.input_preparation(prefix.input_str)
    return t.search(prepared_in_str)

@app.post("/complete/")
def suggest_complete(prefix: InputModel):
    prepared_in_str = data_prep.input_preparation(prefix.input_str)
    r = t.autocomplete(prepared_in_str)
    return r[:20]