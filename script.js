const images = document.querySelectorAll('.banner img');
let currentIndex = 0;

function changeImage() {
    images[currentIndex].classList.add('hidden');
    currentIndex = (currentIndex + 1) % images.length;
    images[currentIndex].classList.remove('hidden');
}

// Change banner image every 2 seconds
setInterval(changeImage, 2000);

function navigateTo(page) {
    window.location.href = page;
}
