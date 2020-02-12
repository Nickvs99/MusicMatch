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

    // TODO absolute path or relate from root or django template
    let data = await fetch("../ajax/validate_username", {
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
    })

    let dataJson = await data.json();

    if (dataJson["usernameTaken"]){
            
        let newElement = document.createElement("Small");
        newElement.innerHTML = "This username already exists";
        newElement.classList.add("inputUsernameError");

        let usernameInputElement = document.getElementById("inputUsername");
        usernameInputElement.parentNode.insertBefore(newElement, usernameInputElement.nextSibling);
    }
}