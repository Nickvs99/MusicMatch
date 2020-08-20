document.addEventListener('DOMContentLoaded', () => {

    // Element with the username input and button for adding/removing extra fields
    // child 0 is the input, child 1 is the button
    let userField = document.getElementById("formUsernames").children[0];
    let addButton = userField.children[1];
    addButton.onclick = addUserField;

	document.getElementById("formUsernames").onsubmit = async () => {

		event.preventDefault();
		event.stopPropagation();

		let ids = ["benefits-list", "stats-page", "input-create-playlist"]
		hideElementsByIds(ids);

		let usernames = getUserNames();

		if(! await processingUsernames(usernames, false)){
			return false;
        }
        
        showElementById("stats-page");

		if(usernames.length == 1){
			createSingleCharts(usernames[0]);
		}
		else {
			console.log("COMPARISON")
			createComparisonCharts(usernames);
		}

		updateTitle("DONE")
		console.log(usernames);
		return false;
    };

    document.getElementById("input-create-playlist").onclick = () => {

        clearMessages();

        let usernames = getUserNames();

        RunCreatePlaylist(usernames);

    }
});

function addUserField() {

    let form = document.getElementById("formUsernames");
  
    // Get the userfield associated with the button
    let userField = this.parentNode;
  
    let clone = userField.cloneNode(true);
    clone.children[0].value = null;
  
    form.insertBefore(clone, document.getElementById("submitForm"));
  
    // Convert this add button to a remove button
    let width = this.offsetWidth;
    this.classList.remove("add-user");
    this.classList.add("remove-user");
    this.innerHTML = "-";
    this.style.width = width + "px";
  
    this.classList.remove("expand")
  
    let button = clone.children[1];
  
    // If the maximum number of fields is required, set the cloned button
    // to an action which does nothing
    if (form.children.length >= 6){
      button.onclick = () => {return false};
      button.classList.remove("add-user");
      button.classList.add("do-nothing");
      button.innerHTML = "O";
      button.style.width = width + "px";
    }
    else {
      button.onclick = addUserField;
    }
  
    // Set the expand animation
    clone.classList.add("expand");
    clone.addEventListener("animationend", () => {
    clone.classList.remove("expand");
  
    });
  
    this.onclick = removeUserField;
  
    return false; 
}
  
function removeUserField() {
  
    // Set the shrink animation
    this.parentNode.classList.add("shrink");
    this.parentNode.addEventListener("animationend", () => {
      this.parentNode.remove();
    });
  
    let form = document.getElementById("formUsernames");
    let lastUserField = form.children[form.children.length - 2].children[1];
  
    // When a userfield is removed, set the last button to an add button
    // since there are now less than the max amount of field.
    if(!lastUserField.classList.contains("add-user")){
      lastUserField.classList.remove("do-nothing");
      lastUserField.classList.add("add-user");
      lastUserField.innerHTML = "+";
      lastUserField.onclick = addUserField
    }
  
    return false;
}

function getUserNames(){

    let usernames = [];

	let userFields = document.getElementsByClassName("user-field");
    for(let userField of userFields){
        let username = userField.children[0].value;
        if (username ==""){
            continue;
        }
    	usernames.push(username);
    }
    return usernames;
}


/**
 * The process of the usernames input. This makes sure that the input is valid, creates and updates profiles.
 * @param {strings[]} usernames the updated users accounts
 * @param {boolean} forced Should the usernames be forced to update
 */
async function processingUsernames(usernames, forced){

    let inValidUsernames = await validateUsernames(usernames);
    
    if(inValidUsernames.length != 0){

        let valid = await validateSpotify(inValidUsernames);

        if(!valid){
            // TODO better title
            updateTitle("Stats")
            return false
        }
    }

    await updateProfiles(usernames, forced);

    return true
}

/**
 * Manages the update procedure for the usernames. Checks if a update is needed
 * and if so updates the profile.
 * @param {strings[]} usernames the updated users accounts
 * @param {boolean} forced Should the usernames be forced to update
 */
async function updateProfiles(usernames, forced){
    
    for(let i in usernames){
        let username = usernames[i];

        let args = {"username": username};

        if(!forced){
            
            updateTitle("Checking for update...");
            
            let vars = {"usernames": username}
            let response = await fetch("/ajax/check_update", getFetchContext(args))

            let data = await response.json();
            
            forced = data["update"];
        }

        if(!forced){
            continue
        } 

        updateTitle(`Updating ${username}'s profile...`);

        await fetch("/ajax/update", getFetchContext(args));

        updateTitle(`Cashing results for ${username}'s profile...`);

        await fetch("/ajax/cache_results", getFetchContext(args)); 

        createMessage("success", `Updated ${username}'s profile`);
        
        updateTitle("Updated profile");
        
    }
}


/**
 * Checks whether the usernames are an entry in the SpotifyUser db.
 * Returns a list with all usernames which are not registered.
 * @param {string[]} usernames
 * 
 * @returns {string[]}  All usernames who are not an entry in the SpotifyUser db.
 */
async function validateUsernames(usernames){
    
    updateTitle("Checking if accounts exist in database.");

    let args = {"usernames": usernames};
    let response = await fetch("/ajax/validate_usernames", getFetchContext(args));

    let data = await response.json();

    inValidUsernames = [];
    for(let username in data){

        if (!data[username]){
            inValidUsernames.push(username);
        }
    }

    return inValidUsernames
}

/**
 * Checks wheter the usernames have a spotify account.
 * @param {string[]} usernames
 * @returns bool true when all usernames have a spotify account
 */
async function validateSpotify(usernames){

    updateTitle("Checking if accounts exist in spotify database.");
    
    let args = {"usernames": usernames};
    let response = await fetch("/ajax/validate_spotify_usernames", getFetchContext(args));

    let data = await response.json();

    if (data["all_valid"]){
        return true
    }

    for(let username in data["usernames"]){

        if(!data["usernames"][username]){
            createMessage("danger", `${username} does not have a spotify account.`);
        }   
    }

    return false
}

/**
 * Updates the innerText of the title div
 * @param {string} title
 */
function updateTitle(title){
    document.getElementById("title").innerText = title;
}

/**
 * Updates the innerText of a div
 * @param {string} id
 * @param {string} text
 */
function innerText(id, text) {
    document.getElementById(id).innerText = text;
}

/**
 * Clears the charts. This is done by removing the old element and then creating 
 * a new element with the same attributes.
 * 
 * TODO seach for a cleaner solution.
 */
function clearCharts(){

    let chartIDs = ["artistChart", "genreChart"];

    for(let id of chartIDs){

        let element = document.getElementById(id);
        let cloneElement = element.cloneNode(false);

        // Set  the elements after the title
        let chartsElement = document.getElementById("charts");
        chartsElement.appendChild(cloneElement);

        
        element.remove();
    }
}

/**
 * Updates the charts based on the usernames
 * @param {string[]} usernames 
 * 
 * TODO more than two users
 */
async function createSingleCharts(username){

    updateTitle("Reading stats for " + username);
    
    hideElementsByIds(["stats-block-1-2", "stats-block-2-2", "stats-block-3-2"]);

    let statsPage = document.getElementById("stats-page");
    statsPage.classList.remove("stats-page-double");
    statsPage.classList.add("stats-page-single");

    let args = {"username": username};
    let response = await fetch("/ajax/stats", getFetchContext(args));

    let data = await response.json()

    let artistCount = data["artist_count"];
    let genreCount = data["genre_count"];


    updateTitle("Stats for " + username);

    statsBlock("stats-block-1-1", data["total_songs"], "Songs");
    
    statsBlock("stats-block-2-1", data["total_artists"], "Artists");
    
    statsBlock("stats-block-3-1", data["total_genres"], "Genres");

    
    createChartBlockSlider("stats-chart-artists", artistCount);
    
    createChartBlockSlider("stats-chart-genres", genreCount);
}

function statsBlock(id, value, label) {
    let statsBlock = document.getElementById(id);
    statsBlock.children[0].innerText = value;
    statsBlock.children[1].innerText = label;
}

/**
 * Updates the charts based on the usernames
 * @param {string[]} usernames 
 * 
 * TODO more than two users
 */
async function createComparisonCharts(usernames){

    updateTitle(`Loading comparison between ${usernames[0]} and ${usernames[1]}`);

    showElementsByIds(["stats-block-1-2", "stats-block-2-2", "stats-block-3-2"]);

    let statsPage = document.getElementById("stats-page");
    statsPage.classList.add("stats-page-double");
    statsPage.classList.remove("stats-page-single");

    // Aquire data
    let args = {"usernames": usernames};
    let response = await fetch("/ajax/compare", getFetchContext(args));

    // Parse to json format
    let data = await response.json();
    console.log(data);

    createChartBlockSlider("stats-chart-artists", data["artist_comparison"]);
    
    createChartBlockSlider("stats-chart-genres", data["genre_comparison"]);

    statsBlock("stats-block-1-1", 55, "Songs in common");
    
    statsBlock("stats-block-1-2", 78, "Unique songs");

    statsBlock("stats-block-2-1", 23, "Artists in common");
    
    statsBlock("stats-block-2-2", 43, "Unique artists");

    statsBlock("stats-block-3-1", 6, "Genres in common");

    statsBlock("stats-block-3-2", 13, "Unique genres");

    updateTitle(`Comparison between ${usernames[0]} and ${usernames[1]}`);
}
/**
 * Create the artist chart.
 * @param {string} id
 * @param {dict} artistCount 
 */
function createChartBlockSlider(id, dict) {

    let chartElement = document.getElementById(id);

    removeChildren(chartElement);
    
    let position = 1;
    for (const [key, value] of Object.entries(dict)) {
        
        createChartBlock(chartElement, position, key, value);

        position += 1;
    }
}

function createChartBlock(parent, position, key, values) {

    let newElement = createElement(parent, "chart-block");

    createElement(newElement, "chart-position-label", `#${position}`);
    createElement(newElement, "chart-key-label", capitalize(`${key}`));  
    
    if(Array.isArray(values)) {
        for(let value of values) {
            createElement(newElement, "chart-value-label", `${value} songs`);
        }
    }
    else {
        createElement(newElement, "chart-value-label", `${values} songs`);
    }
}

/**
 * Creates a bar and pie chart with the data.
 * @param {dict} artistCount 
 * @param {dict} genreCount 
 */
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