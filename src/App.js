import './App.css';
import React, { useState, useEffect} from 'react';
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [fullSuggestion, setFullSuggestion] = useState([])
  const [nextChars, setNextChars] = useState([])
  const [prefix, setPrefix] = useState('')

  function handleChangePrefix(e) {
    setPrefix(e.target.value)
  }

  useEffect(() => {
    axios.post('http://localhost:3100/complete', {input_str: prefix})
    .then( res => {
      console.log(res.data)
      setFullSuggestion(res.data)
    })
    .catch( err => {
      setFullSuggestion(null)
      console.log(err)
    })
  }, [prefix])

  function handleSuggest() {
    axios.post('http://localhost:3100/nextword', {input_str: prefix})
    .then( res => {
      console.log(res.data)
      setNextChars(res.data)
    })
    .catch( err => {
      setNextChars(null)
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
              <label className="inputLabel" for="prefix"><b>Product title</b></label>
              <input type="text" id="prefix" name="prefix" placeholder="Product prefix" onChange={handleChangePrefix} value={prefix}></input>
              {/* <Button className="universal-button" style={{width: "20%"}} onClick={handleSuggest}>Suggest</Button> */}

          </div>
        {/* <div className='container'>
          {
            nextChars && nextChars.map( char => <p> {char.char} : {char.score}</p>)
          }
        </div> */}
        <div className='container'>
          {
            fullSuggestion && fullSuggestion.map( word => <p className='p-update-info'> {word.word}</p>)
          }
        </div>
      </div>
    </div>

  );
}

export default App;
