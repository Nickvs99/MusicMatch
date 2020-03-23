document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("submitForm").onclick = () => {

        let ids = ["inputNewPassword", "inputConfirmPassword"];
        if(allFieldsCheck(ids)){
            document.getElementById("formChangePassword").submit()
        }
    }
});