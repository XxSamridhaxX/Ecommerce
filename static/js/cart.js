var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId:", productId, "Action:", action);

        console.log('USER:', user)
if (user == 'AnonymousUser'){
	addCookieItems(productId, action)
			
}else{
	updateUserOrder(productId, action)
}
    });
}


function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    // console.log('data: ',data);
			location.reload();
			// location.reload() reloads the current page so that the effect of adding or deleting the items are quickly seen
		});
}

function addCookieItems(productId, action)
{
	console.log('User is not authenticated')

	if (action == 'add')
	{
		// if cart object ma productId name ko attribute ma kei value chaina bhane/ exist gardeina bhane
		if (cart[productId]== undefined)
		{
			//productId attribute ko euta nikalne ani quantity ma halne
			cart[productId] = {'quantity':1}
		}
		else
		{
			//if paile dekhi nai cha bhane add action auda hataune
			cart[productId]['quantity']+=1
		}
	}

	if(action == 'remove')
	{
		cart[productId]-=1

		if(cart[productId]['quantity']<=0)
		{
			console.log('Items Should be deleted')
			delete cart[productId]
		}

			
	}

	console.log('art:',cart)
	document.cookie = 'cart='+JSON.stringify(cart) + ";domain=;path=/"
	location.reload()

}