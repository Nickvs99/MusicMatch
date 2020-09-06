/**
 * Dependancies:
 *      legacy/chart_util.js
 *      util.js
 */

 document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("submitForm").onsubmit = () => {
        
        clearMessages();
        clearCharts();
    
        let inputUsernameElement = document.getElementById("inputUsername");
        let username = inputUsernameElement.value
        
        UpdatePage(username);

        return false;
    }
});

/**
 * Updates the content of the page based on the usernames.
 * @param {string[]} usernames 
 */
async function UpdatePage(username){

    if(! await processingUsernames([username], false)){
        return
    }
    UpdateCharts(username);
}

/**
 * Updates the charts based on the usernames
 * @param {string[]} usernames 
 * 
 * TODO more than two users
 */
async function UpdateCharts(username){

    updateTitle("Reading stats for " + username);
    
    let args = {"username": username};
    let response = await fetch("/ajax/stats", getFetchContext(args));

    let data = await responseWrapper(response)

    let artistCount = data["artist_count"];
    let genreCount = data["genre_count"]

    updateTitle("Stats for " + username)

    drawCharts(artistCount, genreCount);
}

/**
 * Creates a bar and pie chart with the data.
 * @param {dict} artistCount 
 * @param {dict} genreCount 
 */
function drawCharts(artistCount, genreCount){

    const maxArtists = 10;
    const maxGenres = 15;

    var ctx = document.getElementById('artistChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(artistCount).slice(0, maxArtists),
            datasets: [{
                label: "Count",
                data: Object.values(artistCount).slice(0, maxArtists),
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
                data: Object.values(genreCount).slice(0, maxGenres),
                backgroundColor: createPieColors(Object.keys(genreCount).length, colors),
                borderColor: 'rgba(255,255,255,255)',
                borderWidth:1,
            }],
        
            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: Object.keys(genreCount).slice(0, maxGenres)
        },
        options: {
            title: {
                display: true,
                text: "Most popular genres"
            },
        }
    });
}

// Colors used for the charts. Format is used for chart.js
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

/**
 * Creates the colors for the pie chart. This is done by looping over colorPalette.
 * @param {int} n The number of colors
 * @param {string[]} colorPalette The available colors
 */
function createPieColors(n, colorPalette){
    
    pieColors = []
    for( let i = 0; i < n; i++){
        pieColors.push(colorPalette[i % colorPalette.length])
    }
    return pieColors
}