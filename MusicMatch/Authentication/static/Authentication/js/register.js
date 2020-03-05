document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("inputUsername").onchange = function(){
        
        // Clear all previous error messages
        let elements = document.getElementsByClassName("inputUsernameError");
        while(elements[0]){
            elements[0].remove();
        }
        
        let usernameInputElement = document.getElementById("inputUsername");
        let username = usernameInputElement.value;

        CheckUsername(username);
    };
});

// Check if username exists
async function CheckUsername(username){

    let args = {"username": username};

    // TODO absolute path or relate from root or django template
    let response = await fetch("/ajax/validate_username", getFetchContext(args));

    let data = await response.json();

    if (data["usernameTaken"]){
            
        let newElement = document.createElement("Small");
        newElement.innerHTML = "This username already exists";
        newElement.classList.add("inputUsernameError");

        let usernameInputElement = document.getElementById("inputUsername");
        usernameInputElement.parentNode.insertBefore(newElement, usernameInputElement.nextSibling);
    }
}