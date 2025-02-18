//Global variable for the map
var map;
var concertList = window.concertList;
var markers = [];
function initMap() {

    function createMarkers(M) {
        for(let x = 0; x < M.length; x++) {
            let marker = {
                venue: M[x]['venue'],
                lat: parseFloat(M[x]['lat']),
                lng: parseFloat(M[x]['lng']),
                artist: M[x]['artist'],
                concertDate: M[x]['date']
            };
            markers.push(marker);
        }
        return markers;
    }
    markers = createMarkers(concertList)
    

    //Custom icons. Will eventually be an icon with the accounts profile picture. Another idea is having an arena icon that gets bigger the more its visited
    //const customIcon = 'https://cdn.discordapp.com/attachments/1005329675289112589/1227503753582874734/2_2_Small.png?ex=6628a4f4&is=66162ff4&hm=62ffdb2ce0ae04ff07cbf84eb3a7b5e53ada5e87efa33d9f4afd70f87e1a75f0&'

    const centerMap = { lat: 42.31435, lng: -70.970284} //Centers on boston
    
    const mapOptions = { //All map options
        center: centerMap,
        zoom: 7,
        disableDefaultUI: true,
        keyboardShortcuts: false,
        mapTypeId: "styled_map",
        maxZoom: 11
    }

    const styledMapType = new google.maps.StyledMapType( //Styled map
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
            elementType: "labels",
            styles: [{visibility: "off"}]
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

    map = new google.maps.Map(document.getElementById("google-map"), mapOptions) // Creates map
        
    map.mapTypes.set("styled_map", styledMapType);

    const infoWindow = new google.maps.InfoWindow({
        minWidth: 200,
        maxWidth: 200
    })

    for(let x = 0; x < markers.length; x++) { // Loops through the markers object and displays all markers
        const marker = new google.maps.Marker({
            position: {lat:markers[x]['lat'], lng: markers[x]['lng']},
            map: map,
        });

        function createInfoWindows() {
            const infoWindowContent = `
                <div class="feh-content">
                    <h3>${markers[x]['venue']}</h3>
                    <address> 
                        <p>${markers[x]['artist']}: ${markers[x]['concertDate']}</p>
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