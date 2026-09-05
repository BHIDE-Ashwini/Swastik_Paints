document.addEventListener("DOMContentLoaded", function () {

function renderProducts() {

    document.querySelectorAll(".product-list").forEach(function (container) {
        container.innerHTML = "";
    });

    products.forEach(function (product) {

        const container = document.getElementById(product.categoryId);

        if (!container) {
            return;
        }

        const productItem = document.createElement("button");

        productItem.className = "product-item";
        productItem.type = "button";

        productItem.dataset.productId = product.id;
        productItem.dataset.productName = product.name;
        productItem.dataset.productCategory = product.category;
        productItem.dataset.productDescription = product.description;
        productItem.dataset.productColour = product.colour;
        productItem.dataset.productColourCode = product.colourCode;
        productItem.dataset.productPrice = product.price;

        productItem.innerHTML = `
            <span class="product-index">
                ${product.id}
            </span>

            <span class="product-details">
                <strong>
                    ${product.name}
                </strong>

                <small>
                    ${product.category}
                </small>
            </span>

            <span class="product-colour">
                <span
                    class="colour-dot"
                    style="--product-colour: ${product.colourCode};"
                ></span>

                ${product.colour}
            </span>

            <span class="product-price">
                ₹${Number(product.price).toLocaleString("en-IN")}
                <small>/ L</small>
            </span>

            <span class="product-action">
                VIEW
                <span>↗</span>
            </span>
        `;

        container.appendChild(productItem);
    });
}

renderProducts();


/* =================================================
   CATEGORY SWITCHING
================================================= */

const categoryButtons = document.querySelectorAll(
    ".product-category-button"
);

const categoryContents = document.querySelectorAll(
    ".product-category-content"
);

categoryButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        const selectedCategory = button.dataset.category;

        categoryButtons.forEach(function (item) {
            item.classList.remove("active");
        });

        categoryContents.forEach(function (content) {
            content.classList.remove("active");
        });

        button.classList.add("active");

        const selectedContent = document.querySelector(
            `[data-content="${selectedCategory}"]`
        );

        if (selectedContent) {
            selectedContent.classList.add("active");
        }
    });
});


/* =================================================
   PRODUCT MODAL
================================================= */

const modal = document.getElementById("productModal");

const modalClose = document.getElementById(
    "productModalClose"
);

const modalOverlay = document.querySelector(
    ".product-modal-overlay"
);

const modalProductName = document.getElementById(
    "modalProductName"
);

const modalProductCategory = document.getElementById(
    "modalProductCategory"
);

const modalProductDescription = document.getElementById(
    "modalProductDescription"
);

const modalProductColour = document.getElementById(
    "modalProductColour"
);

const modalProductPrice = document.getElementById(
    "modalProductPrice"
);

const modalColourDisplay = document.getElementById(
    "modalColourDisplay"
);

const addToCartButton = document.getElementById(
    "addToCartButton"
);


/* =================================================
   CART
================================================= */

let cart = JSON.parse(
    localStorage.getItem("productCart")
) || [];

cart = cart.map(function (item) {

    return {
        ...item,
        quantity: Math.max(
            1,
            Number(item.quantity) || 1
        )
    };

});


const cartCount = document.getElementById(
    "cartCount"
);

const cartPopup = document.getElementById(
    "cartPopup"
);

const cartPopupOverlay = document.querySelector(
    ".cart-popup-overlay"
);

const cartPopupClose = document.getElementById(
    "cartPopupClose"
);

const cartItemsContainer = document.getElementById(
    "cartItems"
);

const cartTotalItems = document.getElementById(
    "cartTotalItems"
);

const cartTotalPrice = document.getElementById(
    "cartTotalPrice"
);

let selectedProduct = null;


/* =================================================
   UPDATE CART COUNT
================================================= */

function updateCartCount() {

    const totalItems = cart.reduce(
        function (total, item) {

            return total + Number(
                item.quantity || 0
            );

        },
        0
    );

    if (cartCount) {
        cartCount.textContent = totalItems;
    }
}

updateCartCount();


/* =================================================
   FORMAT PRICE
================================================= */

function formatPrice(price) {

    return Number(
        price || 0
    ).toLocaleString("en-IN");

}


/* =================================================
   SAVE CART
================================================= */

function saveCart() {

    localStorage.setItem(
        "productCart",
        JSON.stringify(cart)
    );

    updateCartCount();

    renderCart();
}


/* =================================================
   OPEN PRODUCT MODAL
================================================= */

document.addEventListener("click", function (event) {

    const product = event.target.closest(
        ".product-item"
    );

    if (!product) {
        return;
    }


    const name = product.dataset.productName;
    const category = product.dataset.productCategory;
    const description = product.dataset.productDescription;
    const colour = product.dataset.productColour;
    const colourCode = product.dataset.productColourCode;
    const price = product.dataset.productPrice;
    const productId = product.dataset.productId;


    selectedProduct = {

        id: productId,
        name: name,
        category: category,
        description: description,
        colour: colour,
        colourCode: colourCode,
        price: Number(price),
        quantity: 1

    };


    if (modalProductName) {
        modalProductName.textContent = name;
    }

    if (modalProductCategory) {
        modalProductCategory.textContent = category;
    }

    if (modalProductDescription) {
        modalProductDescription.textContent = description;
    }

    if (modalProductColour) {
        modalProductColour.textContent = colour;
    }

    if (modalProductPrice) {
        modalProductPrice.textContent =
            formatPrice(price);
    }

    if (modalColourDisplay) {

        modalColourDisplay.style.setProperty(
            "--modal-product-colour",
            colourCode
        );

    }


    if (addToCartButton) {

        const existingProduct = cart.find(
            function (item) {
                return item.id === selectedProduct.id;
            }
        );


        if (existingProduct) {

            addToCartButton.classList.add("added");

            addToCartButton.innerHTML = `
                <span>ADDED TO CART</span>
                <span>✓</span>
            `;

        } else {

            addToCartButton.classList.remove("added");

            addToCartButton.innerHTML = `
                <span>ADD TO CART</span>
                <span>+</span>
            `;

        }

    }


    if (modal) {

        modal.classList.add("active");

        modal.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.classList.add(
            "modal-open"
        );

    }


    if (modalClose) {
        modalClose.focus();
    }

});


/* =================================================
   ADD TO CART
================================================= */

if (addToCartButton) {

    addToCartButton.addEventListener(
        "click",
        function () {

            if (!selectedProduct) {
                return;
            }


            const existingProduct = cart.find(
                function (item) {

                    return item.id === selectedProduct.id;

                }
            );


            if (existingProduct) {

                existingProduct.quantity =
                    Number(existingProduct.quantity) + 1;

            } else {

                cart.push({
                    ...selectedProduct,
                    quantity: 1
                });

            }


            saveCart();


            addToCartButton.classList.add(
                "added"
            );

            addToCartButton.innerHTML = `
                <span>ADDED TO CART</span>
                <span>✓</span>
            `;

        }
    );

}


/* =================================================
   RENDER CART
================================================= */

function renderCart() {

    if (!cartItemsContainer) {
        return;
    }


    cartItemsContainer.innerHTML = "";


    if (cart.length === 0) {

        cartItemsContainer.innerHTML = `
            <div class="cart-empty">

                <div class="cart-empty-icon">
                    🛒
                </div>

                <h3>
                    Your cart is empty
                </h3>

                <p>
                    Add products from our
                    product catalogue.
                </p>

            </div>
        `;


        if (cartTotalItems) {
            cartTotalItems.textContent = "0";
        }

        if (cartTotalPrice) {
            cartTotalPrice.textContent = "0";
        }

        return;
    }


    cart.forEach(function (item, index) {

        const quantity = Math.max(
            1,
            Number(item.quantity) || 1
        );


        const itemTotal =
            Number(item.price || 0) * quantity;


        const cartItem =
            document.createElement("div");

        cartItem.className = "cart-item";

        cartItem.dataset.id = item.id;


        cartItem.innerHTML = `
            <div
                class="cart-item-colour"
                style="
                    --cart-item-colour:
                    ${item.colourCode};
                "
            ></div>


            <div class="cart-item-info">

                <strong>
                    ${item.name}
                </strong>

                <span>
                    ${item.category}
                </span>

                <small>
                    ₹${formatPrice(item.price)} / L
                </small>

                <strong class="cart-item-total">
                    ₹${formatPrice(itemTotal)}
                </strong>

            </div>


            <div class="cart-item-controls">

                <button
                    type="button"
                    class="cart-quantity-button"
                    data-action="decrease"
                    data-index="${index}"
                    aria-label="Decrease quantity"
                >
                    −
                </button>


                <span class="cart-quantity">
                    ${quantity}
                </span>


                <button
                    type="button"
                    class="cart-quantity-button"
                    data-action="increase"
                    data-index="${index}"
                    aria-label="Increase quantity"
                >
                    +
                </button>

            </div>


            <button
                type="button"
                class="cart-remove-button"
                data-action="remove"
                data-index="${index}"
                aria-label="Remove ${item.name}"
            >
                ×
            </button>
        `;


        cartItemsContainer.appendChild(
            cartItem
        );

    });


    const totalItems = cart.reduce(
        function (total, item) {

            return total +
                Number(item.quantity || 0);

        },
        0
    );


    if (cartTotalItems) {

        cartTotalItems.textContent =
            totalItems;

    }


    const totalPrice = cart.reduce(
        function (total, item) {

            const quantity =
                Number(item.quantity || 0);

            const price =
                Number(item.price || 0);

            return total + (
                price * quantity
            );

        },
        0
    );


    if (cartTotalPrice) {

        cartTotalPrice.textContent =
            formatPrice(totalPrice);

    }

}


/* =================================================
   CART BUTTON ACTIONS
================================================= */

if (cartItemsContainer) {

    cartItemsContainer.addEventListener(
        "click",
        function (event) {

            const button =
                event.target.closest(
                    "button[data-action]"
                );


            if (!button) {
                return;
            }


            const action =
                button.dataset.action;


            const index =
                Number(button.dataset.index);


            if (
                Number.isNaN(index) ||
                !cart[index]
            ) {
                return;
            }


            if (action === "increase") {

                cart[index].quantity =
                    Number(
                        cart[index].quantity
                    ) + 1;

            }


            else if (action === "decrease") {

                cart[index].quantity =
                    Number(
                        cart[index].quantity
                    ) - 1;


                if (cart[index].quantity <= 0) {

                    cart.splice(index, 1);

                }

            }


            else if (action === "remove") {

                cart.splice(index, 1);

            }


            saveCart();

        }
    );

}


/* =================================================
   OPEN CART
================================================= */

const cartButton =
    document.querySelector(".cart-button");


function openCart() {

    if (!cartPopup) {
        return;
    }


    renderCart();


    cartPopup.classList.add("active");

    cartPopup.setAttribute(
        "aria-hidden",
        "false"
    );

    document.body.classList.add(
        "cart-open"
    );

}


/* =================================================
   CLOSE CART
================================================= */

function closeCart() {

    if (!cartPopup) {
        return;
    }


    cartPopup.classList.remove("active");

    cartPopup.setAttribute(
        "aria-hidden",
        "true"
    );

    document.body.classList.remove(
        "cart-open"
    );

}


if (cartButton) {

    cartButton.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            openCart();

        }
    );

}


if (cartPopupClose) {

    cartPopupClose.addEventListener(
        "click",
        closeCart
    );

}


if (cartPopupOverlay) {

    cartPopupOverlay.addEventListener(
        "click",
        closeCart
    );

}


/* =================================================
   CLOSE PRODUCT MODAL
================================================= */

function closeProductModal() {

    if (!modal) {
        return;
    }


    modal.classList.remove("active");

    modal.setAttribute(
        "aria-hidden",
        "true"
    );

    document.body.classList.remove(
        "modal-open"
    );

}


if (modalClose) {

    modalClose.addEventListener(
        "click",
        closeProductModal
    );

}


if (modalOverlay) {

    modalOverlay.addEventListener(
        "click",
        closeProductModal
    );

}


/* =================================================
   ESC KEY
================================================= */

document.addEventListener(
    "keydown",
    function (event) {

        if (event.key !== "Escape") {
            return;
        }


        if (
            modal &&
            modal.classList.contains("active")
        ) {

            closeProductModal();

        }


        if (
            cartPopup &&
            cartPopup.classList.contains("active")
        ) {

            closeCart();

        }

    }
);


/* =================================================
   INITIAL CART RENDER
================================================= */

renderCart();

});
