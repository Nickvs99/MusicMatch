document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("inputUsername").onchange = function(){
        
        // Clear all previous error messages
        let elements = document.getElementsByClassName("inputUsernameError");
        while(elements[0]){
            elements[0].remove();
        }
        
        let usernameInputElement = document.getElementById("inputUsername");
        let username = usernameInputElement.value;
        console.log(username);
        // TODO absolute path or relate from root or django template
        fetch("../ajax/validate_username", {
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
        .then((respone) => {
            return respone.json();
        })
        .then((responseJson) => {
            console.log(responseJson);
            if (responseJson["usernameTaken"]){
            
                let newElement = document.createElement("Small");
                newElement.innerHTML = "This username already exists";
                newElement.classList.add("inputUsernameError");
                usernameInputElement.parentNode.insertBefore(newElement, usernameInputElement.nextSibling);
            }
        });
    };
});