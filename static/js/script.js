// script.js

function fetchQuote() {
  // Fetch a new quote from the JavaScript API
  fetch('/api/new_quote')
    .then(response => response.json())
    .then(data => {
      // Update the JavaScript quote text in the HTML
      document.getElementById('quote').textContent = data.quote;
    })
    .catch(error => {
      console.error('Error fetching JavaScript quote:', error);
    });
}

function fetchPythonQuote() {
  // Fetch a new quote from the Python API
  fetch('/api/new_quote', {
    method: 'POST'
  })
    .then(response => response.json())
    .then(data => {
      // Update the Python quote text in the HTML
      document.getElementById('pythonQuote').textContent = data.quote;
    })
    .catch(error => {
      console.error('Error fetching Python quote:', error);
    });
}
