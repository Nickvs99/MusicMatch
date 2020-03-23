document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("submitForm").onclick = () => {

        let ids = ["inputUsername", "inputEmail"];
        if(allFieldsCheck(ids)){
            document.getElementById("formForgotPassword").submit()
        }
    }
});