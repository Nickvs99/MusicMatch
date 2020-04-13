
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
    


    document.getElementById("button-login").onclick = createLoginScreen;
});



function createLoginScreen(){

  console.log("login")

  let background = document.createElement("div");
  background.classList.add("background");
  let loginForm = document.getElementById("loginBlock");

  let body = document.getElementsByTagName("body")[0];
  body.insertBefore(background, loginForm);

  loginForm.style.display="block";
  loginForm.ba = "blur(0%)";

  background.onclick = () => {
    background.remove();
    loginForm.style.display = "none";
  }

}
