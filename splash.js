document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        document.querySelector(".splash-logo").classList.add("zoom-expand"); // Starts zoom effect

        setTimeout(() => {
            window.location.href = "index.html"; // Opens main page AFTER full zoom completes
        }, 1100); // Wait for zoom animation (1.5s) before opening main page
    }, 2000); // Initial delay before zoom starts
});