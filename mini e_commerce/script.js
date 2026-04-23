// script.js

const products = [
    { id: 1, name: "Wireless Headphones", price: 2500, category: "Audio", img: "https://via.placeholder.com/150" },
    { id: 2, name: "Smart Watch", price: 4500, category: "Wearables", img: "https://via.placeholder.com/150" },
    { id: 3, name: "Gaming Mouse", price: 1200, category: "Peripherals", img: "https://via.placeholder.com/150" },
    { id: 4, name: "Mechanical Keyboard", price: 3800, category: "Peripherals", img: "https://via.placeholder.com/150" }
];

let cart = [];

// 1. Display Products
function renderProducts(items) {
    const container = document.getElementById('product-list');
    container.innerHTML = items.map(p => `
        <div class="product-card">
            <img src="${p.img}" alt="${p.name}">
            <h3>${p.name}</h3>
            <p>₹${p.price}</p>
            <button class="add-btn" onclick="addToCart(${p.id})">Add to Cart</button>
        </div>
    `).join('');
}

// 2. Search Filter
function filterProducts() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filtered = products.filter(p => p.name.toLowerCase().includes(query));
    renderProducts(filtered);
}

// 3. Add to Cart
function addToCart(id) {
    const product = products.find(p => p.id === id);
    const existing = cart.find(item => item.id === id);

    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    updateCartUI();
}

// 4. Update Cart UI & Calculate Total
function updateCartUI() {
    const cartItems = document.getElementById('cartItems');
    const totalAmount = document.getElementById('totalAmount');
    const cartCount = document.getElementById('cartCount');

    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <p>${item.name} (x${item.quantity}) - ₹${item.price * item.quantity}</p>
        </div>
    `).join('');

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    totalAmount.innerText = total;
    cartCount.innerText = cart.length;
}

// Modal Toggle Logic
document.getElementById('cartBtn').onclick = () => document.getElementById('cartModal').style.display = "block";
document.querySelector('.close').onclick = () => document.getElementById('cartModal').style.display = "none";

// Initial Load
renderProducts(products);