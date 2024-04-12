function initMap() {
    var markers = [] // Used to create markers. Eventually will recieve the locatios from the set lists

                /*locationName: 'TD Garden',
                lat: 42.366847947342926, 
                lng: -71.06218814804988,
                address: '100 Legends Way,<br> Boston,<br> MA 02114'*/

    function createMarkers(M) {
        for(let x = 0; x < M.length; x++) {
            let marker = {
                LocationName: M[x][2],  // Assuming venue is at index 3
                lat: M[x][4],  // Assuming lat is at index 5
                lng: M[x][5],  // Assuming long is at index 6
                artist: M[x][0],
                concertDate: M[x][1]
            };
            markers.push(marker);
        }
    }
    
    markers = createMarkers()
    

    //Custom icons. Will eventually be an icon with the accounts profile picture. Another idea is having an arena icon that gets bigger the more its visited
    const customIcon = 'https://cdn.discordapp.com/attachments/1005329675289112589/1227503753582874734/2_2_Small.png?ex=6628a4f4&is=66162ff4&hm=62ffdb2ce0ae04ff07cbf84eb3a7b5e53ada5e87efa33d9f4afd70f87e1a75f0&'

    const centerMap = { lat: 42.31435, lng: -70.970284} //Centers on boston
    
    const mapOptions = {
        center: centerMap,
        zoom: 10,
        disableDefaultUI: true,
        keyboardShortcuts: false,
        mapTypeId: "styled_map"
    }

    const styledMapType = new google.maps.StyledMapType(
        [
        { elementType: "geometry", stylers: [{ color: "#ebe3cd" }] },
        { elementType: "labels.text.fill", stylers: [{ color: "#523735" }] },
        { elementType: "labels.text.stroke", stylers: [{ color: "#f5f1e6" }] },
        {
            featureType: "administrative",
            elementType: "geometry.stroke",
            stylers: [{ color: "#c9b2a6" }],
        },
        {
            featureType: "administrative.neighborhood",
            elementType: "labels",
            stylers: [{ visibility: "off" }],
        },
        {
            featureType: "administrative.land_parcel",
            elementType: "labels",
            stylers: [{ visibility: "off" }],
        },
        {
            featureType: "landscape.natural",
            elementType: "geometry",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "poi",
            elementType: "geometry",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [{ color: "#93817c" }],
        },
        {
            featureType: "poi.park",
            elementType: "geometry.fill",
            stylers: [{ color: "#a5b076" }],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [{ color: "#447530" }],
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "road.arterial",
            elementType: "geometry",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "road.highway.controlled_access",
            elementType: "geometry",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "road.highway.controlled_access",
            elementType: "geometry.stroke",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "road.local",
            elementType: "labels.text.fill",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "transit.line",
            elementType: "geometry",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "transit.line",
            elementType: "labels.text.fill",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "transit.line",
            elementType: "labels.text.stroke",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "transit.station",
            elementType: "geometry",
            stylers: [{ color: "#dfd2ae" }],
        },
        {
            featureType: "water",
            elementType: "geometry.fill",
            stylers: [{ color: "#b9d3c2" }],
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [{ color: "#92998d" }],
        },
        {
            featureType: "road.highway",
            elementType: "labels",
            stylers: [{visibility: "off"}]
        },
        {
            featureType: "road.arterial",
            elementType: "labels",
            stylers: [{visibility: "off"}]
        },
        {
            featureType: "road.local",
            elementType: "labels",
            stylers: [{visibility: "off"}]
        },
        ],
        { name: "Styled Map" },
    );

    const map = new google.maps.Map(document.getElementById("google-map"), mapOptions) // Creates map
        
    map.mapTypes.set("styled_map", styledMapType);

    const infoWindow = new google.maps.InfoWindow({
        minWidth: 200,
        maxWidth: 200
    })

    for(let x = 0; x < markers.length; x++) { // Loops through the markers object and displays all markers
        const marker = new google.maps.Marker({
            position: {lat:markers[x]['lat'], lng: markers[x]['lng']},
            map: map,
            icon: customIcon
        });

        function createInfoWindows() {
            const infoWindowContent = `
                <div class="feh-content">
                    <h3>${markers[x]['locationName']}</h3>
                    <address> 
                        <p>${markers[x]['artist']}<hr>
                            ${markers[x]['concertDate']}</p>
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