document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("inputUsername").onchange = async function(){

        clearMessages();
        validateUsername();    
    };

    document.getElementById("inputPasswordCheck").onchange = function(){

        clearMessages();
        passwordCheck();
    };

    document.getElementById("submitForm").onclick = async function(){
        if(await validateForm()){
            document.getElementById("form").submit()
        }
        
    }
});

/**
 * Checks wheter the form is valid. The form is valid when all fields are filled
 * in, password and confirm password are the same and the username does not yet exist.
 * 
 * @returns bool True when form is valid
 */
async function validateForm(){

    clearMessages();

    // Three seperated if statements are used, since this will display all of the
    // errors. Instead of just one.

    let validForm = true;
    if(!allFieldsCheck()){
        validForm = false;
    }
    if(!passwordCheck()){
        validForm = false;
    }
    if(!await validateUsername()){
        validForm = false;
    }

    console.log(validForm)

    return validForm
} 

/**
 * Checks if the username is an entry in the ExtendedUser db.
 * 
 * @returns bool True when the username does not exist
 */
async function validateUsername(){
    
    let usernameInputElement = document.getElementById("inputUsername");
    let username = usernameInputElement.value;
    
    let args = {"username": username};
    let response = await fetch("/ajax/validate_username", getFetchContext(args));

    let data = await response.json();

    if(!data["valid_username"]){
        createMessage("danger", "This username is already taken");
    }
    return data["valid_username"]    
}

/**
 * Checks if the password and confirm password are the same.
 * 
 * @returns bool
 */
function passwordCheck(){

    let password1 = document.getElementById("inputPassword").value;
    let password2 = document.getElementById("inputPasswordCheck").value;

    if(password1 == password2){
        return true;
    }

    createMessage("danger", "Passwords do not match");

    return false
}

/**
 * Checks if all fields are filled in.
 * 
 * @returns bool
 */
function allFieldsCheck(){

    let elementsID = ["inputUsername", "inputPassword", "inputPasswordCheck", "inputEmail"];
    for(let id of elementsID){
        if(!document.getElementById(id).value){
            createMessage("danger", "All fields are required.");
            return false
        }
    }

    return true
}