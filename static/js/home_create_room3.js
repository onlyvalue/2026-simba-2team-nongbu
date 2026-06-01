const recordChips = document.querySelectorAll(
    '.record-cycle-setting .chip'
);

const recordInput = document.getElementById(
    'recordCycle'
);

recordChips.forEach((chip) => {

    chip.addEventListener('click', () => {

        if (chip.classList.contains('active')) {

            chip.classList.remove('active');
            recordInput.value = '';

        } else {

            recordChips.forEach((c) => {
                c.classList.remove('active');
            });

            chip.classList.add('active');
            recordInput.value = chip.dataset.value;
        }
    });

});

const limitChips = document.querySelectorAll(
    '.limit-chip'
);

const limitInput = document.getElementById(
    'recordLimit'
);

limitChips.forEach((chip) => {

    chip.addEventListener('click', () => {

        if (chip.classList.contains('active')) {

            chip.classList.remove('active');
            limitInput.value = '';

        } else {

            limitChips.forEach((c) => {
                c.classList.remove('active');
            });

            chip.classList.add('active');
            limitInput.value = chip.dataset.value;
        }
    });

});

