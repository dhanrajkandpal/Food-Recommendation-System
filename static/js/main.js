document.addEventListener("DOMContentLoaded", () => {

    "use strict";


    // =====================================================
    // 1. ELEMENTS
    // =====================================================

    const menuToggle = document.getElementById("menuToggle");

    const navLinks = document.getElementById("navLinks");


    // Stop if mobile navigation doesn't exist

    if (!menuToggle || !navLinks) {
        return;
    }


    // =====================================================
    // 2. MENU STATE
    // =====================================================

    function closeMenu() {

        navLinks.classList.remove("active");

        menuToggle.setAttribute(
            "aria-expanded",
            "false"
        );

        menuToggle.textContent = "☰";

    }


    function openMenu() {

        navLinks.classList.add("active");

        menuToggle.setAttribute(
            "aria-expanded",
            "true"
        );

        menuToggle.textContent = "✕";

    }


    function toggleMenu() {

        const isOpen =
            navLinks.classList.contains("active");


        if (isOpen) {

            closeMenu();

        } else {

            openMenu();

        }

    }


    // =====================================================
    // 3. TOGGLE BUTTON
    // =====================================================

    menuToggle.addEventListener(
        "click",
        toggleMenu
    );


    // =====================================================
    // 4. CLOSE AFTER NAVIGATION
    // =====================================================

    const navItems = navLinks.querySelectorAll("a");


    navItems.forEach((item) => {

        item.addEventListener("click", closeMenu);

    });


    // =====================================================
    // 5. CLOSE WHEN CLICKING OUTSIDE
    // =====================================================

    document.addEventListener("click", (event) => {

        const clickedInsideNavigation =
            navLinks.contains(event.target) ||
            menuToggle.contains(event.target);


        if (!clickedInsideNavigation) {

            closeMenu();

        }

    });


    // =====================================================
    // 6. CLOSE WITH ESCAPE KEY
    // =====================================================

    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {

            closeMenu();

            menuToggle.focus();

        }

    });


    // =====================================================
    // 7. RESET MENU WHEN RESIZING TO DESKTOP
    // =====================================================

    window.addEventListener("resize", () => {

        if (window.innerWidth > 600) {

            closeMenu();

        }

    });


    console.log(
        "FITTIN homepage navigation initialized."
    );

});