document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("submitUsername").onclick = () => {
        
        clearMessages();
        clearCharts();
    
        let inputUsernameElement = document.getElementById("inputUsername");
        let username = inputUsernameElement.value
        
        UpdatePage(username);
    }
});

// Updates the stats page for a new username
async function UpdatePage(username){

    let inValidUsernames = await validateUsernames([username]);
    
    if(inValidUsernames.length != 0){

        let valid = await validateSpotify(inValidUsernames);

        if(!valid){
            updateTitle("Stats")
            return 
        }

        await writeData(inValidUsernames);
    }

    UpdateCharts(username);
}

// Updates the charts for a given username. This username has to be in 
// the MM db.
async function UpdateCharts(username){

    updateTitle("Reading stats for " + username);
    let data = await fetch("../ajax/stats", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: "same-origin",
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: JSON.stringify({
            "username": username
        })        
    });

    artistCount = dataJson["artist_count"];
    genreCount = dataJson["genre_count"]

    updateTitle("Stats for " + username)

    drawCharts(artistCount, genreCount);
}

// Checks wheter the usernames are registered in the MM db.
// Returns a list with all usernames which are not registered.
async function validateUsernames(usernames){
    
    updateTitle("Checking if accounts exist in database.");
    let data = await fetch("../ajax/validate_usernames", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: "same-origin",
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: JSON.stringify({
            "usernames": usernames
        })        
    });

    let dataJson = await data.json();

    inValidUsernames = [];
    for(let username in dataJson){

        if (!dataJson[username]){
            inValidUsernames.push(username);
        }
    }

    return inValidUsernames
}

// Checks wheter the usernames have a spotify account.
// Returns true when all usernames have an account, else false.
async function validateSpotify(usernames){

    updateTitle("Checking if accounts exist in spotify database.");
    let data = await fetch("../ajax/validate_spotify_usernames", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: "same-origin",
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: JSON.stringify({
            "usernames": usernames
        })        
    });

    let dataJson = await data.json();

    if (dataJson["all_valid"]){
        return true
    }

    for(let username in dataJson["usernames"]){

        if(!dataJson["usernames"][username]){
            createMessage("danger", `${username} does not have a spotify account.`);
        }   
    }

    return false
}

// Writes the data from the spotify db to the MM db. 
// All usernames need to have a spotify account.
async function writeData(usernames){
    
    for(let i in usernames){
        let username = usernames[i];

        // TODO these function should be able to run asynchronous, however
        // removing the await will result with errors...
        await fetch("../ajax/write_data", {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: "same-origin",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            body: JSON.stringify({
                "username": username
            })        
        });
    }
}

// Update the title 
function updateTitle(title){
    document.getElementById("title").innerText = title;
}

// Clears all messages
function clearMessages(){
    let messages = document.getElementById("messages");
    while(messages.firstChild){
        messages.firstChild.remove();
    }
}

// Clears the charts. This is done by removing the old element and then creating 
// a new element with the same attributes.
// TODO seach for a cleaner solution. 
function clearCharts(){

    // Should be in opposite order of how you want the charts displayed
    let chartIDs = ["genreChart", "artistChart"];

    for(let i in chartIDs){

        let id = chartIDs[i];
        let element = document.getElementById(id);
        let cloneElement = element.cloneNode(false);

        // Set  the elements after the title
        let titleElement = document.getElementById("title");
        titleElement.parentNode.insertBefore(cloneElement, titleElement.nextSibling);

        
        element.remove();

    }

}

// Draws the chart with the given data
function drawCharts(artistCount, genreCount){
    var ctx = document.getElementById('artistChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(artistCount),
            datasets: [{
                label: "Count",
                data: Object.values(artistCount),
                backgroundColor: colors,
                borderColor: borderColors,
                borderWidth: 1 
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            responsive: true,
            title: {
                display: true,
                text: "Most popular artists"
            }
        }
    });

    // Piechart which visualises the genre distribution
    var ctx = document.getElementById('genreChart').getContext('2d');
    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            datasets: [{
                data: Object.values(genreCount),
                backgroundColor: createPieColors(Object.keys(genreCount).length, colors),
                borderColor: 'rgba(255,255,255,255)',
                borderWidth:1,
            }],
        
            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: Object.keys(genreCount)
        },
        options: {
            title: {
                display: true,
                text: "Most popular genres"
            },
        }
    });
}

// Create a information message to the user
function createMessage(context, message){

    // Get parent object of new messageElement
    let messagesElement = document.getElementById("messages");

    let messageElement = document.createElement("div");

    // Bootstraps contextual classes 
    let bootstrapContexts = ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"];
    
    if(bootstrapContexts.includes(context)){
        messageElement.classList.add("alert", "alert-" + context);
        messageElement.innerText = message;
    }
    else {
        console.log(`ERROR: ${context} is an invalid context type. Choose from ${bootstrapContexts}`);
        messageElement.classList.add("alert", "alert-danger");
        messageElement.innerText = message;
    }
    messagesElement.appendChild(messageElement);

}

// Colors used for the charts
var colors = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgba(255, 170, 170, 0.2)',
    'rgba(128, 0,0,0.2)',
    'rgba(210, 245, 60,0.2)',
    'rgba(0,0,128,0.2)',
]

// BorderColors used for the charts
// TODO link them to colors
var borderColors = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)',
    'rgba(255, 170, 170, 1)',
    'rgba(128, 0,0,1)',
    'rgba(210, 245, 60,1)',
    'rgba(0,0,128,1)',
]

// Creates the colors for the pie chart. This is done by looping over colorPalette.
function createPieColors(n, colorPalette){
    
    pieColors = []
    for( let i = 0; i < n; i++){
        pieColors.push(colorPalette[i % colorPalette.length])
    }
    return pieColors
}