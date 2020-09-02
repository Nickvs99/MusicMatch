/**
 * All functions related to the creation of the playlist.
 * 
 * Dependancies:
 *      util.js
 */

document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("input-create-playlist").onclick = () => {

        clearMessages();

        let usernames = getUserNames();

        RunCreatePlaylist(usernames);
    }
});

/**
 * Creates a playlist based on the usernames
 * @param {string[]} usernames 
 */
async function RunCreatePlaylist(usernames){

    if(! await CheckAccesToken()){
        return;
    }

    if(! await processingUsernames(usernames, false)){
        return
    }
    CreatePlaylist(usernames);
}

/**
 * Checks if the current logged in user has an access token.
 * Redirects the user to {verify} if the user doesn't have it.
 * @return bool
 */
async function CheckAccesToken(){

    let response = await fetch("/ajax/check_access_token", getFetchContext({}))

    let data = await response.json();

    if(!data["loggedin"]){

        createMessage("danger", "You have to login to create a playlist.")
        return false;
    }

    if(!data["access_token"]){

        window.location.href = "/verify"
        return false
    }

    return true;
}

/**
 * Creates a playlist for the logged in user based on the songs from the usernames.
 * @param {string[]} usernames 
 */
async function CreatePlaylist(usernames){

    updateTitle("Creating playlist...")

    let args = {"usernames": usernames};

    await fetch("/ajax/playlist", getFetchContext(args));

    createMessage("success", "Successfully created a playlist!")
    
    // Reset title 
    updateTitle(`Comparison between ${usernames[0]} and ${usernames[1]}`);
}
