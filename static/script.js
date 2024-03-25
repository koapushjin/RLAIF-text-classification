function sendTextForPrediction() {
    const textInput = document.getElementById('textInput').value;
    fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: textInput
            }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('predictionResult').innerHTML = `Model Prediction: ${data.prediction}, Confidence Level: ${data.confidence}`;
            // document.getElementById('predictionResult').innerHTML = `Model Prediction: ${data.prediction}, Confidence Level: ${data.confidence}, Entropy Score: ${data.entropy}`;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function sendAnnotationForUpdate(correctedLabel) {
    const textInput = document.getElementById('textInput').value;
    fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: textInput,
                label: correctedLabel
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.log('Error:', error);
        });
}

console.log('hello')
