document.getElementById('sentiment-form').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent form from submitting the traditional way
    
    const textInput = document.getElementById('text-input').value;
    
    if (!textInput) {
        alert('Please enter some text!');
        return;
    }

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerText = 'Error: ' + data.error;
        } else {
            resultDiv.innerHTML = `
                <p>Sentiment: <strong>${data.sentiment}</strong> (Confidence: ${(data.score * 100).toFixed(2)}%)</p>
                <p>${data.message}</p>
            `;
        }
    })
    .catch(err => {
        console.error('Error:', err);
    });
});

