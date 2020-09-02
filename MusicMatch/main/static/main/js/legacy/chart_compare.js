/**
 * Dependancies:
 *      legacy/chart_util.js
 *      util.js
 */

 document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("formCompare").onsubmit = () => {
        
        clearMessages();
        clearCharts();
        
        // TODO create function for getting usernames
        let inputUsername1Element = document.getElementById("inputUsername1");
        let username1 = inputUsername1Element.value

        let inputUsername2Element = document.getElementById("inputUsername2");
        let username2 = inputUsername2Element.value
        
        UpdatePage([username1, username2]);

        return false;
    }
        
    document.getElementById("inputCreatePlaylist").onclick = () => {

        clearMessages()

        let inputUsername1Element = document.getElementById("inputUsername1");
        let username1 = inputUsername1Element.value;

        let inputUsername2Element = document.getElementById("inputUsername2");
        let username2 = inputUsername2Element.value;

        RunCreatePlaylist([username1, username2]);

    }
});

/**
 * Updates the content of the page based on the usernames.
 * @param {string[]} usernames 
 */
async function UpdatePage(usernames){

    if(! await processingUsernames(usernames, false)){
        return
    }

    UpdateCharts(usernames);
}

/**
 * Creates a playlist based on the usernames
 * @param {string[]} usernames 
 */
async function RunCreatePlaylist(usernames){

    if(! await CheckAccesToken()){
        return;
    }

    if(! await processingUsernames(usernames, false)){
        return
    }
    CreatePlaylist(usernames);
}

/**
 * Updates the charts based on the usernames
 * @param {string[]} usernames 
 * 
 * TODO more than two users
 */
async function UpdateCharts(usernames){

    updateTitle(`Loading comparison between ${usernames[0]} and ${usernames[1]}`);

    // Aquire data
    let args = {"usernames": usernames};
    let response = await fetch("/ajax/compare", getFetchContext(args));

    // Parse to json format
    let data = await response.json();

    let artists = data["artists"];
    let user1ArtistCount = data["user1_artist_count"];
    let user2ArtistCount = data["user2_artist_count"];

    let genres = data["genres"];
    let user1GenreCount = data["user1_genre_count"];
    let user2GenreCount = data["user2_genre_count"];

    // Update charts
    horizontalBarChart("artistChart", usernames, artists, user1ArtistCount, user2ArtistCount, "Most in common artists");
    horizontalBarChart("genreChart", usernames, genres, user1GenreCount, user2GenreCount, "Most in common genres");

    updateTitle(`Comparison between ${usernames[0]} and ${usernames[1]}`);
}

/**
 * Creates a horizontal barchart
 * @param {string} id The html id
 * @param {string[]} usernames 
 * @param {string[]} labels The labels for the datasets
 * @param {dict} data1 
 * @param {dict} data2 
 * @param {string} title The title of the chart
 */
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

/**
 * Checks if the current logged in user has an access token.
 * Redirects the user to {verify} if the user doesn't have it.
 * @return bool
 */
async function CheckAccesToken(){

    let response = await fetch("/ajax/check_access_token", getFetchContext({}))

    let data = await response.json();

    if(!data["loggedin"]){

        createMessage("danger", "You have to login to create a playlist.")
        return false;
    }

    if(!data["access_token"]){

        window.location.href = "/verify"
        return false
    }

    return true;
}

/**
 * Creates a playlist for the logged in user based on the songs from the usernames.
 * @param {string[]} usernames 
 */
async function CreatePlaylist(usernames){

    updateTitle("Creating playlist...")

    let args = {"usernames": usernames};

    await fetch("/ajax/playlist", getFetchContext(args));

    createMessage("success", "Successfully created a playlist!")
    
    updateTitle(`Comparison between ${usernames[0]} and ${usernames[1]}`);
}