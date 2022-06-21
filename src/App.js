import './App.css';
import React, { useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import TitleGenService from "./service"

function App() {
  const [fullSuggestion, setFullSuggestion] = useState([])
  const [prefix, setPrefix] = useState('')

  function handleChangePrefix(e) {
    setPrefix(e.target.value)
  }

  useEffect(() => {
    if ( prefix.length < 1) {
      setFullSuggestion([])
    } else{
      TitleGenService.autoComplete({prefix:prefix.toLowerCase()})
      .then( res => {
        // console.log(res.data)
        if (res.data.length > 0) {
          setFullSuggestion(res.data)
        }
      })
      .catch( err => {
        setFullSuggestion(null)
        console.log(err)
      })
    }
    
  }, [prefix])

  return (
    <div className='App'>

      <div className="background">
      
          <div className="container">
              <label className="inputLabel" for="prefix"><b>Product title</b></label>
              <input type="text" id="prefix" name="prefix" placeholder="Product prefix" onChange={handleChangePrefix} value={prefix}></input>

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
