document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("formUpdate").onsubmit = () => {
        
        clearMessages();

        let inputUsernameElement = document.getElementById("inputUsername");
        let username = inputUsernameElement.value;

        processingUsernames([username], true);

        return false
    }
});