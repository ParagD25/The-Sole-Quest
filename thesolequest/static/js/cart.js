var UpdateButtons=document.getElementsByClassName('update-cart-button')

for(var i=0;i<UpdateButtons.length;i++){
    UpdateButtons[i].addEventListener('click',function(){
        var productID=this.dataset.product
        var action=this.dataset.action

        if (user=='AnonymousUser'){
            console.log('Not logged in')
        }
        else{
            updateUserOrder(productID,action)
        }

    })

}

function updateUserOrder(productID,action){
    console.log('User is logged in, sending data..')

    var url='/update-cart/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productID':productID,'action':action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('Data:',data)
        location.reload()
    })
}