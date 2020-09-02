/**
 * Dependencies:
 *      auth.js
 *      util.js
 */

 document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("formUpdate").onsubmit = async () => {
        
        event.preventDefault();
        event.stopPropagation();

        clearMessages();

        let inputUsernameElement = document.getElementById("inputUsername");
        let username = inputUsernameElement.value;

        await processingUsernames([username], true);

        updateTitle("Update profile");

        return false
    }
});