const input = document.getElementById('input');
const categories = document.getElementById('categories');
const resultDiv = document.getElementById('result_div')
input.onkeyup = getSuggestion;

function removeElementChildren(element) {
    while( element.firstChild) {
        element.removeChild(element.firstChild)
    }
}

function displaySuggestion(data) {
    if ( data.length > 0 ) {
        removeElementChildren(resultDiv)
        for(let i = 0; i < data.length; i++ ) {
            var suggestion = document.createElement("p");
            suggestion.setAttribute("id", `sug${i}`);
            suggestion.innerHTML = data[i].title;
            resultDiv.appendChild(suggestion);
        }
    }
}

async function getSuggestion(e) {
    var prefix = input.value
    if (prefix.length > 0) {
        var data = { 
            prefix: prefix,
            category: categories.value,
            top_n: 20,
            max_length: 100
        }

        const response = await fetch('/api/autocomplete', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body:   JSON.stringify(data)
        })
        .catch( err => console.log(err))
    
        const responseData = await response.json();
        displaySuggestion(responseData)
    }
    else {
        removeElementChildren(resultDiv)
    }
}