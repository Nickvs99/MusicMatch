/**
 * Sets the values for a statsBlock specified by its id
 * @param {string} id 
 * @param {string} value 
 * @param {string} label 
 */
function statsBlock(id, value, label) {
    let statsBlock = document.getElementById(id);
    statsBlock.children[0].innerText = value;
    statsBlock.children[1].innerText = label;
}
