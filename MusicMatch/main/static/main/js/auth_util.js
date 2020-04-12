// Set of functions used in the authorisation pages 

/**
 * Checks if the password and confirm password are the same.
 * 
 * @returns bool
 */
function passwordCheck(){

    let password1 = document.getElementById("inputNewPassword").value;
    let password2 = document.getElementById("inputConfirmPassword").value;

    let confirmField = document.getElementById("inputConfirmPassword").parentNode;
    removeErrorMessages(confirmField);

    if(password1 == password2){
        return true;
    }

    addErrorMessage(confirmField, "Passwords do not match");

    return false;
}

/**
 * Checks if all fields are filled in.
 * 
 * @param {strings[]} ids ids of the fields
 * @returns bool
 */
function allFieldsCheck(ids){

    let valid = true;
    for(let id of ids){
        let el = document.getElementById(id)  
        if(!el.value){ 

            addErrorMessage(el.parentNode, "This field is required");
            valid = false;
        }
    }

    return valid
}

function removeErrorMessages(element){
    for(let child of element.children){

        // remove message
        if(child.classList.contains("error-text")){
            child.remove();
        }

        // remove invalid style on input
        if(child.classList.contains("input-text")){
            child.classList.remove("invalid-input");
        }
    }
}

function addErrorMessage(parent, message){

    let errorElement = document.createElement("small");
    errorElement.classList.add("error-text");
    errorElement.innerHTML = message;

    parent.appendChild(errorElement);
    for(let child of parent.children){
        if(child.classList.contains("input-text")){
            child.classList.add("invalid-input")
        }
    }
}