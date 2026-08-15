document.addEventListener("DOMContentLoaded", function () {

    const categoryButtons =
        document.querySelectorAll(".product-category-button");

    const categoryContents =
        document.querySelectorAll(".product-category-content");


    categoryButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const selectedCategory =
                button.dataset.category;


            /*
             * Remove active state
             * from all category buttons
             */

            categoryButtons.forEach(function (item) {

                item.classList.remove("active");

            });


            /*
             * Hide all product sections
             */

            categoryContents.forEach(function (content) {

                content.classList.remove("active");

            });


            /*
             * Activate selected category
             */

            button.classList.add("active");


            /*
             * Show selected products
             */

            const selectedContent =
                document.querySelector(
                    `[data-content="${selectedCategory}"]`
                );


            if (selectedContent) {

                selectedContent.classList.add("active");

            }

        });

    });

});