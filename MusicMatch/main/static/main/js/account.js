document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("editEmail").onclick = () => {

        hideElementsByIds(["emailValue", "editEmail"]);
        showElementsByIds(["inputEmail", "saveEmail"]);
    }

    document.getElementById("saveEmail").onclick = async () => {

        clearMessages();

        let emailValue = document.getElementById("inputEmail").value;
        if (emailValue == ""){
            createMessage("danger", "Your email has to have a value.");
            return
        }
        
        let args = {"email": emailValue};
        let response = await fetch("/ajax/set_email", getFetchContext(args));

        hideElementsByIds(["inputEmail", "saveEmail"]); 
        showElementsByIds(["emailValue", "editEmail"]);

        createMessage("success", "Successfully changed email.");

        document.getElementById("emailValue").innerHTML = emailValue;
    }


    document.getElementById("editSpotifyAccount").onclick = () => {
        window.location.href = "/verify"
    }

    document.getElementById("editPassword").onclick = () => {
        hideElementsByIds(["editPassword"]);
        showElementsByIds(["formResetPassword"])
    }

    document.getElementById("formResetPassword").onsubmit = () => {

        clearMessages();

        let ids = ["inputOldPassword", "inputNewPassword", "inputConfirmPassword"]
        if(allFieldsCheck(ids) && passwordCheck()){
            document.getElementById("formResetPassword").submit()
        }
    }
});

