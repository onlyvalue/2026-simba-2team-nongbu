const passwordBtn = document.querySelector('.user-info button:nth-of-type(1)');
const nicknameBtn = document.querySelector('.user-info button:nth-of-type(2)');
const logoutBtn = document.querySelector('.more-menu button:nth-of-type(1)');
const deleteBtn = document.querySelector('.more-menu button:nth-of-type(2)');
const logoutModal = document.getElementById('logoutModal');
const logoutCancel = document.getElementById('logoutCancel');
const logoutConfirm = document.getElementById('logoutConfirm');
const deleteAccountModel = document.getElementById('deleteAccountModel');
const deleteCancel = document.getElementById('deleteCancel');
const deleteConfirm = document.getElementById('deleteConfirm');

passwordBtn.addEventListener('click', () => {
    window.location.href = '/mypage/password/';
});

nicknameBtn.addEventListener('click', () => {
    window.location.href = '/mypage/nickname/';
});

logoutBtn.addEventListener('click', () => {
    logoutModal.classList.add('active');
});

logoutCancel.addEventListener('click', () => {
    logoutModal.classList.remove('active');
});

logoutConfirm.addEventListener('click', () => {
    window.location.href = '/account/logout/';
});

deleteBtn.addEventListener('click', () => {
    deleteAccountModel.classList.add('active');
});

deleteCancel.addEventListener('click', () => {
    deleteAccountModel.classList.remove('active');
});

deleteConfirm.addEventListener('click', () => {
    window.location.href = '/account/delete_account/';
});
