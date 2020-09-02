/**
 * All functions related to the userfields on the home page.
 * 
 * Userfield
 *      Input: username input
 *      Button: add userField state and remove userField state    
 *      
 */
    

document.addEventListener('DOMContentLoaded', () => {

    // Element with the username input and button for adding/removing extra fields
    // child 0 is the input, child 1 is the button
    let userField = document.getElementById("formUsernames").children[0];
    let addButton = userField.children[1];
    addButton.onclick = addUserField;
});

/**
 * Get the usernames from all the userFields
 * 
 * @return string[] usernames
 */
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

function addUserField() {

    const maxUserField = 2;

    let form = document.getElementById("formUsernames");
  
    // Get the userfield associated with the button
    let userField = this.parentNode;
  
    let clone = userField.cloneNode(true);
    clone.children[0].value = null;
    
    // TODO prototype
    userField.parentNode.insertBefore(clone, userField.nextSibling);
  
    // Convert this add button to a remove button
    let width = this.offsetWidth;
    this.classList.remove("add-user");
    this.classList.add("remove-user");
    this.innerHTML = "-";
    this.style.width = width + "px";
  
    this.classList.remove("expand")
    this.onclick = removeUserField;

    let button = clone.children[1];
  
    // If the maximum number of fields is required, set the cloned button
    // to an action which does nothing
    if (form.children.length >= maxUserField + 1) {
        button.classList.remove("add-user");
        button.classList.add("remove-user");
        button.innerHTML = "-";
        button.style.width = width + "px";

        button.onclick = removeUserField;
    }
    else {
        button.onclick = addUserField;
    }
  
    // Set the expand animation
    clone.classList.add("expand");
    clone.addEventListener("animationend", () => {
        clone.classList.remove("expand");
    });
    
    return false; 
}
  
function removeUserField() {
  
    // Set the shrink animation
    this.parentNode.classList.add("shrink");
    this.parentNode.addEventListener("animationend", () => {
      this.parentNode.remove();
    });

    // Remove the user-field-button class so it doesn't show up in element searches
    this.classList.remove("user-field-button");
  
    let form = document.getElementById("formUsernames");
    let activeButtons = form.getElementsByClassName("user-field-button");

    if(activeButtons.length == 0) {
        return false;
    }

    let lastActiveButton = activeButtons[activeButtons.length - 1];
  
    // When a userfield is removed, set the last button to an add button
    // since there are now less than the max amount of field.
    lastActiveButton.classList.remove("remove-user");
    lastActiveButton.classList.add("add-user");
    lastActiveButton.innerHTML = "+";
    lastActiveButton.onclick = addUserField;
    
    return false;
}
