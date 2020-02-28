// Set of functions the stats pages need. Like validation etc.

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