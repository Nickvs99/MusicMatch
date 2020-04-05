// Set of functions used in the authorisation pages 

/**
 * Checks if the password and confirm password are the same.
 * 
 * @returns bool
 */
function passwordCheck(){

    let password1 = document.getElementById("inputNewPassword").value;
    let password2 = document.getElementById("inputConfirmPassword").value;

    if(password1 == password2){
        return true;
    }

    createMessage("danger", "Passwords do not match");

    return false
}

/**
 * Checks if all fields are filled in.
 * 
 * @param {strings[]} ids ids of the fields
 * @returns bool
 */
function allFieldsCheck(ids){

    for(let id of ids){
        if(!document.getElementById(id).value){
            createMessage("danger", "All fields are required.");
            return false
        }
    }

    return true
}