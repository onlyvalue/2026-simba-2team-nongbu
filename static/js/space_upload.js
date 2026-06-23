const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const cameraIcon = document.getElementById("cameraIcon");
const addImageBtn = document.querySelector(".add-image-btn");

// 플러스 버튼 클릭 시 파일 선택창 열기
addImageBtn.addEventListener("click", (e) => {
    e.preventDefault();
    imageInput.click();
});

// 파일 선택 시 미리보기
imageInput.addEventListener("change", function () {
    const file = this.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (e) {
        previewImage.src = e.target.result;

        // 사진 표시
        previewImage.style.display = "block";

        // 카메라 아이콘 숨기기
        cameraIcon.style.display = "none";
    };

    reader.readAsDataURL(file);
});

// 하루 1개 제한
const errorMsg = document.getElementById('errorMsg');

if (errorMsg) {
    setTimeout(() => {
        errorMsg.classList.add('hide');

        setTimeout(() => {
            errorMsg.remove();
        }, 500);

    }, 1500);
}