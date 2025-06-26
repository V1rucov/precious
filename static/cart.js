document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(elems, {direction: "left"});

    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});

function addToCart() {
    const size = document.getElementById('size-select').value;
    const color = document.getElementById('color-select').value;

    if (!size || !color) {
        alert("Пожалуйста, выберите размер и цвет!");
        return;
    }

    fetch('/cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            product_id: "{{ product.id }}",
            size: size,
            color: color
        })
    }).then(response => {
        if (response.ok) {
            alert("Товар добавлен в корзину!");
        } else {
            alert("Ошибка при добавлении в корзину!");
        }
    });
    setTimeout(function(){ loadCart(); }, 500);
}

function sendOrder() {
    let contacts = prompt("Введите ваш номер телефона или Telegram: наш менеджер свяжется с вами для оплаты и согласования доставки");
    if (!contacts) {
        alert("Контакты обязательны!");
        return;
    }

    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    fetch('/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contacts: contacts, items: cart })
    }).then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => alert("Ошибка при отправке заказа"));
}

function loadCart() {
    const cartItems = document.getElementById('cart-items');
    fetch(`/cart?_=${Date.now()}`)
        .then(response => response.json())
        .then(data => {
            cartItems.innerHTML = ''; // Очистить старые элементы
            const buttonContainer = document.getElementById('order-button-container');
            buttonContainer.innerHTML = ''; // Убрать кнопку, если она уже есть

            if (data.length === 0) {
                cartItems.innerHTML = '<li class="collection-item">Пока пусто(</li>';
                return; 
            }

            data.forEach((item, index) => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="row" style="display: flex; align-items: center;">
                        <div style="flex: 0 0 auto; margin-right: 10px;">
                            <a onclick="removeFromCart(${index})">
                                <i class="material-icons" style="color: red; cursor: pointer;">close</i>
                            </a>
                        </div>
                        <div style="flex: 1;">
                            <p style="margin: 0;">
                                ${item.product.name} (${item.size || 'No size'}, ${item.color || 'No color'})
                            </p>
                        </div>
                    </div>`;
                cartItems.appendChild(li);
            });

            // Добавим кнопку "Заказать"
            const li2 = document.createElement('li');
            li2.innerHTML = `<div class="buy_button center-align" onClick="sendOrder()">заказать</div>`;
            cartItems.appendChild(li2);
        });
}

function removeFromCart(index) {
    fetch(`/cart/${index}`, { method: 'DELETE' })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка удаления');
            return response.text(); // или .json(), если сервер возвращает данные
        }).catch(err => console.error(err));
    setTimeout(function(){ loadCart(); }, 500);
}