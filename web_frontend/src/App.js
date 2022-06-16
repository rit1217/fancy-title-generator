import './App.css';
import React, { useState, useEffect} from 'react';
import axios from "axios";
import { Button } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [fullSuggestion, setFullSuggestion] = useState([])
  const [nextWords, setNextWords] = useState([])
  const [prefix, setPrefix] = useState('')

  function handleChangePrefix(e) {
    setPrefix(e.target.value)
  }

  function handleSuggest() {
    axios.post('http://localhost:3100/nextword', {input_str: prefix})
    .then( res => {
      console.log(res.data)
      setNextWords(res.data)
    })
    .catch( err => {
      setNextWords(null)
      console.log(err)
    })

    axios.post('http://localhost:3100/complete', {input_str: prefix})
    .then( res => {
      console.log(res.data)
      setFullSuggestion(res.data)
    })
    .catch( err => {
      setFullSuggestion(null)
      console.log(err)
    })

  }

  return (
    <div className='App'>

      <div className="background">
      
          <div className="container">
              <label className="inputLabel" for="prefix">Product title</label>
              <input type="text" id="prefix" name="prefix" placeholder="Product prefix" onChange={handleChangePrefix} value={prefix}></input>
              <Button className="universal-button" style={{width: "20%"}} onClick={handleSuggest}>Suggest</Button>

          </div>
        <div className='container'>
          {
            nextWords && nextWords.map( word => <p> {word.word} : {word.score}</p>)
          }
        </div>
        <div className='container'>
          {
            fullSuggestion && fullSuggestion.map( word => <p> {word.word} : {word.score}</p>)
          }
        </div>
      </div>
    </div>

  );
}

export default App;
