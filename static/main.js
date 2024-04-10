function initMap() {

    const markers = [ // Used to create markers. Eventually will recieve the locatios from the set lists
        {
            locationName: 'TD Garden',
            lat: 42.366847947342926, 
            lng: -71.06218814804988,
            address: '100 Legends Way,<br> Boston,<br> MA 02114'
        }
        
    ];

    const centerMap = { lat: 42.31435, lng: -70.970284} //Centers on boston
    
    const mapOptions = {
        center: centerMap,
        zoom: 10,
        disableDefaultUI: true,
    }

    const map = new google.maps.Map(document.getElementById("google-map"), mapOptions) // Creates map
        
    for(let x = 0; x < markers.length; x++) { // Loops through the markers object and displays all markers
        const marker = new google.maps.Marker({
            position: {lat:markers[0]['lat'], lng: markers[0]['lng']},
            map: map
        });
    }   
}
    /*
    // Initialize and add the map
            function initMap() {
            map = new google.maps.Map(document.getElementById("map"), {
                center: { lat: -34.397, lng: 150.644 },
                zoom: 6,
            });
            infoWindow = new google.maps.InfoWindow();

            const locationButton = document.createElement("button");

            locationButton.textContent = "Pan to Current Location";
            locationButton.classList.add("custom-map-control-button");
            map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
            locationButton.addEventListener("click", () => {
                // Try HTML5 geolocation.
                if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };

                    infoWindow.setPosition(pos);
                    infoWindow.setContent("Location found.");
                    infoWindow.open(map);
                    map.setCenter(pos);
                    },
                    () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                    },
                );
                } else {
                // Browser doesn't support Geolocation
                handleLocationError(false, infoWindow, map.getCenter());
                }
            });
        }
            } */