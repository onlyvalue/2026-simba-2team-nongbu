// ===== FAB 버튼 =====

const fabBtn = document.getElementById('fabBtn');
const fabContainer = document.querySelector('.fab-container');
const fabOverlay = document.getElementById('fabOverlay');

fabBtn.addEventListener('click', () => {

    fabContainer.classList.toggle('active');
    fabOverlay.classList.toggle('active');

});

fabOverlay.addEventListener('click', () => {

    fabContainer.classList.remove('active');
    fabOverlay.classList.remove('active');

});


// ===== 메뉴 버튼 =====

const menuBtn = document.getElementById('menuBtn');
const menuOverlay = document.getElementById('menuOverlay');
const spaceMenu = document.getElementById('spaceMenu');

menuBtn.addEventListener('click', () => {

    menuOverlay.classList.add('active');
    spaceMenu.classList.add('active');

});

menuOverlay.addEventListener('click', () => {

    menuOverlay.classList.remove('active');
    spaceMenu.classList.remove('active');

});


// ===== 업로드 =====

const upLoadBtn = document.getElementById('upLoadBtn');

upLoadBtn.addEventListener('click', () => {

    window.location.href = "{% url 'space_upload' %}";
})