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

/**
 * Removes all children from the parent element
 * @param {*} parent 
 */
function removeChildren(parent) {

    while(parent.firstChild) {
        parent.firstChild.remove();
    }
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function hideElementById(id) {
    console.log(id)
    document.getElementById(id).classList.add("hidden");
}

function hideElementsByIds(ids){
	for(let id of ids) {
        hideElementById(id);
	}
}

function showElementById(id) {
    document.getElementById(id).classList.remove("hidden");
}

function showElementsByIds(ids){	
	for(let id of ids) {
        showElementById(id);
	}
}

function createElement(parent, cssClass, text) {
    let element = document.createElement("div");
    element.classList.add(cssClass);
    parent.appendChild(element);

    if(arguments.length == 3) {
        element.innerText = text;
    }

    return element;
}

/**
 * Appends a string to the end of all the items of the values
 * @param {string} values 
 * @param {string} valueSuffix 
 */
function appendSuffix(values, valueSuffix) {

    if (Array.isArray(values)) {

        let returnValues = [];
        for(let i = 0; i < values.length; i++) {
            returnValues.push(values[i] + valueSuffix);
        }

        return returnValues;
    }
    else {
        return values + valueSuffix;
    }
}