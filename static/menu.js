var concerts = [];
//Displays the search function to add concerts
function showSearchAndDatePicker() {
    var searchAndResults = document.querySelector('#menuContent');
        searchAndResults.innerHTML = `
            <form id="searchForm">
                <input type="text" name="query" class="searchBar" placeholder="Artist...">
                <input type="date" name="date" class="datePicker">
                <input type="submit" value="Submit" class="searchButton">
            </form>
            <button onclick="displayConcerts()" id="backButton">Back</button>
            <div id="results"></div>
        `;

    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from being submitted normally

        var query = document.querySelector('.searchBar').value;
        var date = document.querySelector('.datePicker').value;

        // Send an AJAX request
        $.ajax({
            url: '/search',
            method: 'POST',
            data: {
                query: query,
                date: date
            },
            success: function(response) {
                console.log(response);
                var resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = ``;  // Clear any existing results

                concerts = response;
                // Loop through the results and add them to the results div
                resultsDiv.innerHTML += `<div class="container">`;
                for (var i = 0; i < response.length; i++) {
                    var result = response[i];
                    var resultHTML = `
                        <div class="box" onclick="toggleInfo(this)">
                            <h3>${result.artist}, ${result.date}</h3>
                            <div class="arrow"></div>
                            <div class="button_plus" onclick="addConcert(${i})"></div>
                            <div class="info">
                                Venue: ${result.venue}, ${result.city} <br>
                                Setlist: <br>
                        `;
                        for (var j = 0; j < result.set.length; j++) {
                            resultHTML += `${result.set[j]}<br>`;
                        }
                    resultsDiv.innerHTML += resultHTML+`</div></div>`;
                }
                resultsDiv.innerHTML += `</div>`;
            }
        });
    });
}

function displayConcerts() {
    var concertList = window.concertList;
    console.log(concertList);
    var resultsDiv = document.querySelector('#menuContent');
    resultsDiv.innerHTML = `<button onclick="showMenuOptions()" id="backButton">Back</button>
                            <div id="results"></div>`;
    var concertDiv = document.getElementById('results');
    concertDiv.innerHTML += `<div class="container">`;
    for (var i = 0; i < concertList.length; i++) {  
        var concert = concertList[i];
        var resultHTML = `
            <div class="box" onclick="toggleInfo(this)">
                <h3>${concert.artist}, ${concert.date}</h3>
                <div class="arrow"></div>
                <div class="info">
                    Venue: ${concert.venue}, ${concert.city} <br>
                    Setlist: <br>
            `;
            for (var j = 0; j < concert.songList.length; j++) {
                resultHTML += `${concert.songList[j]}<br>`;
            }
        concertDiv.innerHTML += resultHTML+`</div></div>`;
    }
    concertDiv.innerHTML += `</div>
                             <div class="button_plus" onclick="showSearchAndDatePicker()"></div>`;

}

//Sends added concert to /storedata to add concert to the database
function addConcert(index) { // Adds a concert to a server side variable
    //alert('Added ' + concert.artist + ' to your list of concerts!');
    concert = concerts[index]
    const artist=concert.artist;
    const date=concert.date;
    const venue=concert.venue;
    const lat=concert.lat;
    const lng=concert.lng;
    const songList=concert.set;
    console.log(concerts[index]);
    selectedResult = [{artist, date, venue, lat, lng, songList}];
    $.ajax({
        url: '/storedata',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(selectedResult),
        success: function() {
            console.log("Data stored successfully");
        },
        error: function(response){
            console.log("Error:", response.responseText);
            alert('Failed to add concert!');
        }
    });
}

//Displays extrainfo
function toggleInfo(element) {
    var info = element.getElementsByClassName('info')[0];
    if (info.style.display !== "block") {
        info.style.display = "block";
        element.classList.add('open')
    } else {
        info.style.display = "none";
        element.classList.remove('open')
    }
}

//Animates menu button
function changePos(x) {
    x.classList.toggle('change');
    }

//Moves the menu on screen
function toggleMenu() {
    var menu = document.getElementById('menu');
    menu.classList.toggle('open');
}

//Display menu options again
function showMenuOptions() {
    var menuContent = document.querySelector('#menuContent');
    menuContent.innerHTML = `
        <div class="menuButtonOptions">
            <a href="#" onclick="displayConcerts()" class="menuOptions">Concert List</a>
            <div class="menuOptions">Friends List</div>
            <div class="menuOptions">Settings</div> 
        </div>`;
}