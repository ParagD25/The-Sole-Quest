window.toast = function(str, extraClass = '', timeout = 3000) {  
    const div = document.createElement('div')
    div.className = 'toast ' + extraClass
    div.innerHTML = str  
    setTimeout(function(){
      div.remove()
    }, timeout);
    document.body.appendChild(div);  
}