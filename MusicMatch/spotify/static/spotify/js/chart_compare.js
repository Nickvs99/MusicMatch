document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("submitUsernames").onclick = () => {
        
        clearMessages();
        clearCharts();
        
        // TODO create function for getting usernames
        let inputUsername1Element = document.getElementById("inputUsername1");
        let username1 = inputUsername1Element.value

        let inputUsername2Element = document.getElementById("inputUsername2");
        let username2 = inputUsername2Element.value
        
        UpdatePage([username1, username2]);
    }
        
    document.getElementById("inputCreatePlaylist").onclick = () => {

        clearMessages()

        let inputUsername1Element = document.getElementById("inputUsername1");
        let username1 = inputUsername1Element.value;

        let inputUsername2Element = document.getElementById("inputUsername2");
        let username2 = inputUsername2Element.value;

        RunCreatePlaylist([username1, username2])

    }
});

// Updated the page
async function UpdatePage(usernames){

    if(await validate_usernames(usernames)){
        UpdateCharts(usernames[0], usernames[1]);   
    }
}

// Run the creation of the playlist
async function RunCreatePlaylist(usernames){
    if(await validate_usernames(usernames)){

        CreatePlaylist(usernames[0], usernames[1]);
    }
}

// Updates the charts based on the two usernames
async function UpdateCharts(username1, username2){

    updateTitle(`Loading comparison between ${username1} and ${username2}`);

    // Aquire data
    let data = await fetch("../ajax/compare", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: "same-origin",
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: JSON.stringify({
            "username1": username1,
            "username2": username2
        })  
    });

    // Parse to json format
    let dataJson = await data.json();

    let artists = dataJson["artists"];
    let user1ArtistCount = dataJson["user1_artist_count"];
    let user2ArtistCount = dataJson["user2_artist_count"];

    let genres = dataJson["genres"];
    let user1GenreCount = dataJson["user1_genre_count"];
    let user2GenreCount = dataJson["user2_genre_count"];

    // Update charts
    horizontalBarChart("artistChart", username1, username2, artists, user1ArtistCount, user2ArtistCount, "Most in common artists");
    horizontalBarChart("genreChart", username1, username2, genres, user1GenreCount, user2GenreCount, "Most in common genres");

    updateTitle(`Comparison between ${username1} and ${username2}`);
}

// Checks if all given usernames have a spotify account
async function validate_usernames(usernames){

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

    for(let username in dataJson["usernames"]){

        if(!dataJson["usernames"][username]){
            createMessage("danger", username +" is not found in the database");  
        }
    }
    
    return dataJson["all_valid"]
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

    let parentElement = document.getElementById("charts");

    // Get all chart ids and remove old charts
    let ids = [];
    let charts = document.getElementsByClassName("chart");
    while(charts[0]){
        ids.push(charts[0].id);
        charts[0].remove();
    }
    
    for(let i in ids){

        let id = ids[i];
        let canvas = document.createElement("canvas");
        canvas.id = id;

        // Set the ratio of the canvas element to 1:1
        canvas.width = 1;
        canvas.height = 1;

        canvas.classList.add("chart")

        parentElement.appendChild(canvas);
    }
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

// Creates a horizontal bar chart with two datasets.
function horizontalBarChart(id, username1, username2, labels, data1, data2, title){

    // Checks if element exists
    var element = document.getElementById(id);
    if (!element){
        return;
    }
    
    var ctx = element.getContext('2d');
    var myGenreChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels,
            datasets: [{
                label: username1,
                data: data1,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,

            },{
                label: username2,
                data: data2,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
            }],
        },
        options: {
            scales: {
                xAxes: [{
                    display: true,
                    ticks: {
                        beginAtZero: true,
                    }
                }]
            },
            title: {
                display: true,
                text: title,
            },
            responsive: true,
        }
    });
}

async function CreatePlaylist(username1, username2){

    updateTitle("Creating playlist...")

    let data = await fetch("../ajax/playlist", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: "same-origin",
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: JSON.stringify({
            "username1": username1,
            "username2": username2
        }) 
    });

    let dataJson = await data.json();

    // Check if another error occured
    if(dataJson["error"]){

        createMessage("danger", dataJson["error"]);

        // If the error message has something to say about a access_token
        if (dataJson["error"].includes("access_token")){

            window.location.href = "../verify";
        }
        return
    }

    createMessage("success", "Successfully created a playlist!")
    updateTitle(`Comparison between ${username1} and ${username2}`);

}