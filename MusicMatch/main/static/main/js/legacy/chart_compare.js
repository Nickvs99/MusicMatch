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
    let data = await responseWrapper(response);

    let artistComparison = data["artist_comparison"];
    let genreComparison = data["genre_comparison"];

    // Update charts
    horizontalBarChart("artistChart", usernames, artistComparison, "Most in common artists", 10);
    horizontalBarChart("genreChart", usernames, genreComparison, "Most in common genres", 10);

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
function horizontalBarChart(id, usernames, dict_comparison, title, n){

    let labels = Object.keys(dict_comparison).slice(0, n);

    let data1 = [];
    let data2 = [];

    let count = 0;
    for(let label of labels) {
        let values = dict_comparison[label];

        data1.push(values[0]);
        data2.push(values[1]);
    }

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

    let data = await responseWrapper(response);

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