/**
 * Dependencies:
 *      form_util.js
 *      util.js
 */
document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("inputUsername").onchange = async function(){

        clearMessages();
        validateUsername();    
    };

    document.getElementById("inputConfirmPassword").onchange = () => {

        clearMessages();
        passwordCheck();
    };

    document.getElementById("formRegister").onsubmit = async () => {

        // Since this is a async function the default behauviour is stopped
        event.preventDefault();
        event.stopPropagation();

        let valid = await validateForm();
        if(valid){
            document.getElementById("formRegister").submit()
        }
        return false;
    }
});

/**
 * Checks wheter the form is valid. The form is valid when all fields are filled
 * in, password and confirm password are the same and the username does not yet exist.
 * 
 * @returns bool True when form is valid
 */
async function validateForm(){


    // Three seperated if statements are used, since this will display all of the
    // errors. Instead of just one.

    let validForm = true;
    let ids = ["inputUsername", "inputNewPassword", "inputConfirmPassword", "inputEmail"];
    for(let id of ids){
        let el = document.getElementById(id).parentNode;
        removeErrorMessages(el);
    }
    if(!allFieldsCheck(ids)){
        validForm = false;
    }
    if(!passwordCheck()){
        validForm = false;
    }
    if(!await validateUsername()){
        validForm = false;
    }

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

    // Remove possible previous error message
    let userField = usernameInputElement.parentNode;
    removeErrorMessages(userField);
    
    let args = {"username": username};
    let response = await fetch("/ajax/validate_username", getFetchContext(args));

    let data = await responseWrapper(response);

    if(!data["valid_username"]){
        let userField = usernameInputElement.parentNode;
        
        addErrorMessage(userField, "This username is already taken");
    }
    return data["valid_username"]    
}
