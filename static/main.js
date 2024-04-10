function initMap() {

    const markers = [ // Used to create markers. Eventually will recieve the locatios from the set lists
        {
            locationName: 'TD Garden',
            lat: 42.366847947342926, 
            lng: -71.06218814804988,
            address: '100 Legends Way,<br> Boston,<br> MA 02114'
        }
        
    ];

    //Custom icons. Will eventually be an icon with the accounts profile picture (maybe)
    const customIcon = 'https://cdn.discordapp.com/attachments/1005329675289112589/1227503753582874734/2_2_Small.png?ex=6628a4f4&is=66162ff4&hm=62ffdb2ce0ae04ff07cbf84eb3a7b5e53ada5e87efa33d9f4afd70f87e1a75f0&'

    const centerMap = { lat: 42.31435, lng: -70.970284} //Centers on boston
    
    const mapOptions = {
        center: centerMap,
        zoom: 10,
        disableDefaultUI: true,
    }

    const map = new google.maps.Map(document.getElementById("google-map"), mapOptions) // Creates map
        
    const infoWindow = new google.maps.InfoWindow({
        minWidth: 200,
        maxWidth: 200
    })

    for(let x = 0; x < markers.length; x++) { // Loops through the markers object and displays all markers
        const marker = new google.maps.Marker({
            position: {lat:markers[0]['lat'], lng: markers[0]['lng']},
            map: map,
            icon: customIcon
        });

        function createInfoWindows() {
            const infoWindowContent = `
                <div class="feh-content">
                    <h3>${markers[x]['locationName']}</h3>
                    <address> 
                        <p>${markers[x]['address']}</p>
                    </address>
                </div>
            `;
            google.maps.event.addListener(marker, 'click', function() {
                infoWindow.setContent(infoWindowContent);
                infoWindow.open(map, marker);
            });
        }
        createInfoWindows();
        
    }   
}