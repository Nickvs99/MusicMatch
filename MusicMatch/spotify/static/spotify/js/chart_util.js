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

        if(!forced){
            
            updateTitle("Checking for update...");

            let data = await fetch("../ajax/check_update", {
                method: "post",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                mode: "same-origin",
                headers: {'X-CSRFToken': Cookies.get('csrftoken')},
                body: JSON.stringify({
                    "username": username,
                })  
            })

            let dataJson = await data.json();
            
            forced = dataJson["update"];
        }

        if(!forced){
            continue
        } 

        updateTitle(`Updating ${username}'s profile...`);

        await fetch("../ajax/update", {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: "same-origin",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            body: JSON.stringify({
                "username": username,
            })   
        });

        updateTitle(`Cashing results for ${username}'s profile...`);

        await fetch("../ajax/cache_results", {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: "same-origin",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            body: JSON.stringify({
                "username": username,
            })   
        }); 

        createMessage("success", `Updated ${username}'s profile`);
        
        updateTitle("Updated profile");
        
    }
}


/**
 * Checks whether the usernames are an entry in the UserProfile db.
 * Returns a list with all usernames which are not registered.
 * @param {string[]} usernames
 * 
 * @returns {string[]}  All usernames who are not an entry in the UserProfile db.
 */
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

/**
 * Checks wheter the usernames have a spotify account.
 * @param {string[]} usernames
 * @returns bool true when all usernames have a spotify account
 */
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

/**
 * Updates the innerText of the title div
 * @param {string} title
 */
function updateTitle(title){
    document.getElementById("title").innerText = title;
}

/**
 * Removes all child elements of the messages div.
 */
function clearMessages(){
    let messages = document.getElementById("messages");
    while(messages.firstChild){
        messages.firstChild.remove();
    }
}



/**
 * Clears the charts. This is done by removing the old element and then creating 
 * a new element with the same attributes.
 * 
 * TODO seach for a cleaner solution.
 */
function clearCharts(){

    let chartIDs = ["artistChart", "genreChart"];

    for(let i in chartIDs){

        let id = chartIDs[i];
        let element = document.getElementById(id);
        let cloneElement = element.cloneNode(false);

        // Set  the elements after the title
        let chartsElement = document.getElementById("charts");
        chartsElement.appendChild(cloneElement);

        
        element.remove();
    }
}

/**
 * Create a information message to the user
 * @param {string} context Choises are one of 
 *          ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]
 * @param {*} message The message which has to be displayed.
 */
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