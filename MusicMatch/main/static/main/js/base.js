
document.addEventListener('DOMContentLoaded', () => {
    
    var coll = document.getElementsByClassName("collapsible");
    
    for (let i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", () => {
            var content = coll[i].nextElementSibling;
            if (content.style.maxHeight){
                content.style.maxHeight = null;
              } else {
                content.style.maxHeight = content.scrollHeight + "px";
              }
        });
    }
    
    // Element with the username input and button for adding/removing extra fields
    // child 0 is the input, child 1 is the button
    let userField = document.getElementById("formUsernames").children[0];
    let addButton = userField.children[1];
    addButton.onclick = addUserField;
});

function addUserField() {

  let form = document.getElementById("formUsernames");

  // Get the userfield associated with the button
  let userField = this.parentNode;

  let clone = userField.cloneNode(true);
  clone.children[1].value = null;

  form.insertBefore(clone, document.getElementById("submitForm"));

  // Convert this add button to a remove button
  let width = this.offsetWidth;
  this.classList.remove("add-user");
  this.classList.add("remove-user");
  this.innerHTML = "-";
  this.style.width = width + "px";

  this.classList.remove("expand")

  let button = clone.children[1];

  // If the maximum number of fields is required, set the cloned button
  // to an action which does nothing
  if (form.children.length >= 6){
    button.onclick = () => {return false};
    button.classList.remove("add-user");
    button.classList.add("do-nothing");
    button.innerHTML = "O";
    button.style.width = width + "px";
  }
  else {
    button.onclick = addUserField;
  }

  // Set the expand animation
  clone.classList.add("expand");
  clone.addEventListener("animationend", () => {
  clone.classList.remove("expand");

  });

  this.onclick = removeUserField;

  return false; 
}

function removeUserField() {

  // Set the shrink animation
  this.parentNode.classList.add("shrink");
  this.parentNode.addEventListener("animationend", () => {
    this.parentNode.remove();
  });

  let form = document.getElementById("formUsernames");
  let lastUserField = form.children[form.children.length - 2].children[1];

  // When a userfield is removed, set the last button to an add button
  // since there are now less than the max amount of field.
  if(!lastUserField.classList.contains("add-user")){
    lastUserField.classList.remove("do-nothing");
    lastUserField.classList.add("add-user");
    lastUserField.innerHTML = "+";
    lastUserField.onclick = addUserField
  }

  return false;
}
