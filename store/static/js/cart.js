var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function(){
  var productId = this.dataset.product
  var action = this.dataset.action
  console.log('productId: ', productId, ' action: ', action)
  if (user == 'AnonymousUser') {
    // console.log('Not an authenticaed user');
    addCookieItem(productId, action)
  } else {
    updateUserOrder(productId, action);
  }})
}

function addCookieItem(productId, action) {
  console.log("usernot authenticated", productId, action)
  if (action == 'add') {
    if (cart[productId] == undefined) {
      cart[productId] = {'quantity': 1}
    } else {
      cart[productId]['quantity'] += 1
    }
  }
  if ( action == 'remove') {
    cart[productId]['quantity'] -= 1

    if (cart[productId]['quantity'] <= 0){
      console.log("item deleted")
      delete cart[productId]
    }
  }
  console.log(cart)
  document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
  location.reload();
}

function updateUserOrder(productId, action) {
  console.log("User is logged in. Sending data...");
  console.log('from cart.js', csrftoken)
  var url = '/update_item/'
  fetch(url, {
    method: 'POST',
    header: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({'productId': productId, 'action': action})
  })

  .then((response) => {response.json()})

  .then((data) => {
    // console.log(data)
    location.reload()
  })
}
