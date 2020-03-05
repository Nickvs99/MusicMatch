document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("submitUsername").onclick = () => {
        
        clearMessages();

        let inputUsernameElement = document.getElementById("inputUsername");
        let username = inputUsernameElement.value;

        processingUsernames([username], true)
    }
});