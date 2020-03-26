document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("editEmail").onclick = function(){

        document.getElementById("emailValue").style.display = "none";
        document.getElementById("inputEmail").style.display = "block";
        document.getElementById("editEmail").style.display = "none";
        document.getElementById("saveEmail").style.display = "block";

    }

    document.getElementById("saveEmail").onclick = async function(){

        clearMessages();

        document.getElementById("emailValue").style.display = "block";
        document.getElementById("inputEmail").style.display = "none";
        document.getElementById("editEmail").style.display = "block";
        document.getElementById("saveEmail").style.display = "none";

        let emailValue = document.getElementById("inputEmail").value;
        if (emailValue == ""){
            createMessage("danger", "Your email has to have a value.");
            return
        }
        
        let args = {"email": emailValue};
        let response = await fetch("/ajax/set_email", getFetchContext(args));

        createMessage("success", "Successfully changed email.");

        document.getElementById("emailValue").innerHTML = emailValue;
    }


    document.getElementById("editSpotifyAccount").onclick = function(){
        window.location.href = "/verify"
    }

    document.getElementById("editPassword").onclick = function(){
        document.getElementById("formResetPassword").style.display = "block";
        this.style.display = "none";
    }

    document.getElementById("formResetPassword").onsubmit = function(){

        clearMessages();

        let ids = ["inputOldPassword", "inputNewPassword", "inputConfirmPassword"]
        if(allFieldsCheck(ids) && passwordCheck()){
            document.getElementById("formResetPassword").submit()
        }
    }
});

