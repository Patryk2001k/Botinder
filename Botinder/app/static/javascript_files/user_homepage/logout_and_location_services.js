function logout(element){
    var logoutUrl = element.dataset.logoutUrl;
    window.location.href = logoutUrl;
}

function askForLocation() {
    navigator.geolocation.watchPosition(function(position) {
        var data = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        }
    
        fetch('http://127.0.0.1:5000/get_geolocation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }); 
}

askForLocation();
