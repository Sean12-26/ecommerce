var updateBtns = document.getElementsByClassName('update-cart')


for (var i = 0; i < updateBtns.length; i++) {
    // 为每个按钮添加点击事件监听器
    updateBtns[i].addEventListener('click', function () {
        // 获取按钮上的自定义数据
        var productId = this.dataset.product;
        var action = this.dataset.action;

        // 输出日志，显示 productId 和 action
        console.log('productId is:', productId, 'action:', action);

        // 输出用户信息
        console.log('USER:', user);

        // 检查用户是否为匿名用户
        if (user === 'AnonymousUser') {
            addCookieItem(productId,action);
        } else {
            // 如果用户不是匿名用户，则调用 updateUserOrder 函数
            updateUserOrder(productId, action);
        }
    });
}
function addCookieItem(productId,action){
    if (action == 'add'){
        if( cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }
        else{
            cart[productId]['quantity'] += 1}
    }
    if (action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Item should be deleted');
            delete cart[productId];
            console.log('Item already deleted');
        }
    }

    console.log('Cart:',cart )
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
    //console.log('cart:',cart)
    }  



function updateUserOrder(productId, action) {
    // 构建请求的 URL
    var url = '/update_item/';
    console.log('URL:', url);

    // 使用 fetch 函数发起 POST 请求
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,  // 在请求头中添加 CSRF 令牌
        },
        body: JSON.stringify({  // 将数据转换为 JSON 字符串并放入请求体中
            'productId': productId,
            'action': action
        })
    })
    //.then處理成功的情況
    .then((response) => {
        // 处理响应，将响应的 JSON 数据提取出来
        return response.json();
    })
    .then((data) => {
        // 处理提取出的 JSON 数据
        console.log('data:', data);
        location.reload()
    });
}



