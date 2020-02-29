document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("submitUsername").onclick = () => {
        
        clearMessages();

        let inputUsernameElement = document.getElementById("inputUsername");
        let username = inputUsernameElement.value;

        updateProfile(username)
    }
});

async function updateProfile(username){
    
    let inValidUsernames = await validateUsernames([username]);
    
    if(inValidUsernames.length != 0){
        console.log("notvalid")
        let valid = await validateSpotify(inValidUsernames);
        console.log("valid" + valid)
        if(!valid){
            updateTitle("Update")
            return 
        }
    }

    updateTitle("Updating profile...");

    await fetch("../ajax/update", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: "same-origin",
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: JSON.stringify({
            "username": username
        })   
    });

    createMessage("success", `Updated ${username}'s profile`);
    
    updateTitle("Updated profile");

}