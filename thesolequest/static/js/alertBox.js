// All Alerts

window.toast = function(str, extraClass = '', timeout = 3000) {
  const div = document.createElement('div')
  div.className = 'toast ' + extraClass
  div.innerHTML = str
  setTimeout(function(){
    div.remove()
  }, timeout);
  document.body.appendChild(div);
}



const loginBtn = document.querySelector("#login-btn-alert");

if (loginBtn){
  loginBtn.addEventListener("click", () => {
    sessionStorage.setItem("alert", JSON.stringify({show: true, message: "Login Successfull",type: "success"}));
  });

}


const signupBtn = document.querySelector("#signup-btn-alert");

if (signupBtn){
  signupBtn.addEventListener("click", () => {
    sessionStorage.setItem("alert", JSON.stringify({show: true, message: "Account has been Created",type: "success"}));
  });

}

const cartBtn = document.querySelector("#cart-btn-alert");

if (cartBtn){
  cartBtn.addEventListener("click", () => {
    sessionStorage.setItem("alert", JSON.stringify({show: true, message: "Added to Cart",type: "info"}));
  });

}



(() => {
  const alert = sessionStorage.getItem("alert");
  if(alert){
    console.log(alert);
    const alertObj = JSON.parse(alert);
    if(alertObj.show){
      toast(alertObj.message, alertObj.type);
      sessionStorage.setItem("alert", JSON.stringify({show: false, message: ""}));
    }
  }

})();