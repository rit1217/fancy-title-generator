from fastapi import FastAPI
from pydantic import BaseModel
from trie_model.trie import Trie
import model.data_prep as data_prep
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]


app = FastAPI()

data2 = data_prep.data2_preparation('../data/fashionData2.csv')
data1 = data_prep.data1_preparation('../data/fashionProducts.csv')
print( data2[:10])
print( data1[:10])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

t = Trie()
t.add_data(data1)
t.add_data(data2)

class InputModel(BaseModel):
    input_str: str

@app.post("/nextword/")
def suggest_next_word(prefix: InputModel):
    return t.get_next_char(prefix.input_str)[:20]

@app.post("/complete/")
def suggest_complete(prefix: InputModel):
    r = t.autocomplete(prefix.input_str)
    return r[:20]