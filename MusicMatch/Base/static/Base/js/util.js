// Set of functions all pages might needS


/**
 * Returns the context for a fetch request
 * 
 * @param {dict} dict Dictionary with the variables used by the server.
 */
function getFetchContext(dict){
    
    return {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: "same-origin",
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: JSON.stringify(dict)
    }
}