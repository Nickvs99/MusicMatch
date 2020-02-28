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

    let inValidUsernames = await validateUsernames(usernames);
    
    if(inValidUsernames.length != 0){

        let valid = await validateSpotify(inValidUsernames);

        if(!valid){
            updateTitle("Stats")
            return 
        }

        await writeData(inValidUsernames);
    }

    UpdateCharts(usernames);
}

// Run the creation of the playlist
async function RunCreatePlaylist(usernames){

    let inValidUsernames = await validateUsernames(usernames);
    
    if(inValidUsernames.length != 0){

        let valid = await validateSpotify(inValidUsernames);

        if(!valid){
            updateTitle("Stats")
            return 
        }

        await writeData(inValidUsernames);
    }

    CreatePlaylist(usernames[0], usernames[1]);
    
}

// Updates the charts based on the two usernames
// TODO more than two users
async function UpdateCharts(usernames){

    updateTitle(`Loading comparison between ${usernames[0]} and ${usernames[1]}`);

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
            "usernames": usernames,
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
    horizontalBarChart("artistChart", usernames, artists, user1ArtistCount, user2ArtistCount, "Most in common artists");
    horizontalBarChart("genreChart", usernames, genres, user1GenreCount, user2GenreCount, "Most in common genres");

    updateTitle(`Comparison between ${usernames[0]} and ${usernames[1]}`);
}

// Creates a horizontal bar chart with two datasets.
function horizontalBarChart(id, usernames, labels, data1, data2, title){

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
                label: usernames[0],
                data: data1,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,

            },{
                label: usernames[1],
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