document.addEventListener("DOMContentLoaded", () => {

    const menuToggle = document.getElementById("menuToggle");

    const navLinks = document.getElementById("navLinks");


    // ======================================
    // MOBILE NAVIGATION
    // ======================================

    if (!menuToggle || !navLinks) {
        return;
    }


    menuToggle.addEventListener("click", () => {

        const isOpen = navLinks.classList.toggle("active");

        menuToggle.setAttribute(
            "aria-expanded",
            String(isOpen)
        );

        menuToggle.textContent = isOpen ? "✕" : "☰";

    });


    // ======================================
    // CLOSE MENU AFTER CLICKING A LINK
    // ======================================

    const navItems = navLinks.querySelectorAll("a");


    navItems.forEach((item) => {

        item.addEventListener("click", () => {

            navLinks.classList.remove("active");

            menuToggle.setAttribute(
                "aria-expanded",
                "false"
            );

            menuToggle.textContent = "☰";

        });

    });


    // ======================================
    // CLOSE MENU WHEN CLICKING OUTSIDE
    // ======================================

    document.addEventListener("click", (event) => {

        const clickedInsideMenu =
            navLinks.contains(event.target) ||
            menuToggle.contains(event.target);


        if (!clickedInsideMenu) {

            navLinks.classList.remove("active");

            menuToggle.setAttribute(
                "aria-expanded",
                "false"
            );

            menuToggle.textContent = "☰";

        }

    });

});