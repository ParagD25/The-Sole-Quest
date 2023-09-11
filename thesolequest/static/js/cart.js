var UpdateButtons=document.getElementsByClassName('update-cart-button')

for(var i=0;i<UpdateButtons.length;i++){
    UpdateButtons[i].addEventListener('click',function(){
        var productID=this.dataset.product
        var action=this.dataset.action

        if (user=='AnonymousUser'){
            addIteminCookie(productID,action)
        }
        else{
            updateUserOrder(productID,action)
        }

    })

}

function addIteminCookie(productID,action){

    console.log("You are not logged in / Cookie is not set yet")

    if (action=='add'){
        if (cart[productID]==undefined){
            cart[productID]={'quantity':1}
        }
        else{
            cart[productID]['quantity']+=1
        }
    }

    if (action=='remove'){
        cart[productID]['quantity']-=1

        if (cart[productID]['quantity']<=0){
            console.log('Item Would be deleted from the cart !!')
            delete cart[productID]
        }
    }

    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"

    location.reload()
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