// Set of functions the stats pages might need. Like validation etc.


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

