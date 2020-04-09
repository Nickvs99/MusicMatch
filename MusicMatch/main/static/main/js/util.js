// Set of functions all pages might needS


/**
 * Returns the context for a fetch request
 * 
 * @param {dict} dict Dictionary with the variables used by the server.
 */
function getFetchContext(dict){
    
    return {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: "same-origin",
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: JSON.stringify(dict)
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

/**
 * Removes all child elements of the messages div.
 */
function clearMessages(){
    let messages = document.getElementById("messages");
    while(messages.firstChild){
        messages.firstChild.remove();
    }
}