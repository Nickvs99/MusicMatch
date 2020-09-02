/**
 * Dependencies:
 *      form_util.js
 */

document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("formChangePassword").onsubmit = () => {

        let ids = ["inputNewPassword", "inputConfirmPassword"];
        if(allFieldsCheck(ids)){
            return true;
        }
        return false;
    }
});