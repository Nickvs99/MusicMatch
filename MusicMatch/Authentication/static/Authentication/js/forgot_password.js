document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("submitForm").onsubmit = () => {

        let ids = ["inputUsername", "inputEmail"];
        if(allFieldsCheck(ids)){
            return true;
        }
        return false;
    }
});