const container = document.querySelector('.onboarding-container');

let currentPage = 0;

const totalPages = 3;
const slideWidth = 100 / totalPages;

function moveSlide() {
    container.style.transform = `translateX(-${currentPage * slideWidth}%)`;
}

let startX = 0;
let endX = 0;

container.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
});

container.addEventListener('touchend', (e) => {
    endX = e.changedTouches[0].clientX;

    const diff = startX - endX;

    // 왼쪽으로 스와이프
    if (diff > 50) {
        if (currentPage < totalPages - 1) {
            currentPage++;
            moveSlide();
        }
    }

    // 오른쪽으로 스와이프
    if (diff < -50) {
        if (currentPage > 0) {
            currentPage--;
            moveSlide();
        }
    }
});