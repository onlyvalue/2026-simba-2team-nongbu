const spaceRoom = document.querySelector('.space-room');
const spaceMap = document.getElementById('spaceMap');
const svg = document.getElementById('constellation-svg');

const constellations = JSON.parse(
    document.getElementById('constellations-data').textContent
);

constellations.forEach(item => {

    const stars = item.data.stars;
    const lines = item.data.lines;
    const currentStarCount = item.required; // 임시테스트 코드 바꿔야함 const currentStarCount = item.current;

    const offsetX = item.data.world_x;
    const offsetY = item.data.world_y;

    // 선
    lines.forEach(([startIdx, endIdx]) => {

        if (
            startIdx >= currentStarCount ||
            endIdx >= currentStarCount
        ) {
            return;
        }

        const start = stars[startIdx];
        const end = stars[endIdx];

        const line = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "line"
        );

        line.setAttribute(
            "x1",
            start[0] + offsetX
        );

        line.setAttribute(
            "y1",
            start[1] + offsetY
        );

        line.setAttribute(
            "x2",
            end[0] + offsetX
        );

        line.setAttribute(
            "y2",
            end[1] + offsetY
        );

        line.setAttribute("stroke", "white");
        line.setAttribute("stroke-width", "1");

        svg.appendChild(line);
    });

    // 별
    stars
        .slice(0, currentStarCount)
        .forEach(([x, y]) => {

            const star = document.createElementNS(
                "http://www.w3.org/2000/svg",
                "image"
            );

            star.setAttribute(
                "href",
                "/static/images/star.svg"
            );

            star.setAttribute(
                "x",
                x + offsetX - 8
            );

            star.setAttribute(
                "y",
                y + offsetY - 8
            );

            star.setAttribute("width", "19");
            star.setAttribute("height", "19");

            svg.appendChild(star);
        });

    // 이름
    const info = document.createElement('div');

    info.className = 'constellation-info';

    info.style.position = 'absolute';

    const maxX = Math.max(
        ...stars.map(star => star[0])
    );

    const minX = Math.min(
        ...stars.map(star => star[0])
    );

    const minY = Math.min(
        ...stars.map(star => star[1])
    );

    const maxY = Math.max(
        ...stars.map(star => star[1])
    );

    const centerY = (minY + maxY) / 2;

    if (item.data.label_position === "right") {

        info.style.left =
            `${offsetX + maxX + 15}px`;

        info.style.top =
            `${offsetY + centerY - 20}px`;

    } else {

        info.style.left =
            `${offsetX + minX - 80}px`;

        info.style.top =
            `${offsetY + centerY - 20}px`;
    }

    info.innerHTML = `
        <div class="constellation-name">
            ${item.name}
        </div>
    `;

    spaceMap.appendChild(info);
});

const resetViewBtn =
    document.getElementById('resetViewBtn');

const HOME_X = -200;
const HOME_Y = -250;
const HOME_SCALE = 1;

// ===== 우주 드래그 =====

let isDragging = false;

let startX = 0;
let startY = 0;

let currentX = HOME_X;
let currentY = HOME_Y;

let scale = HOME_SCALE;

spaceMap.style.transform =
    `translate(${currentX}px, ${currentY}px)
    scale(${scale})`;

spaceRoom.addEventListener('mousedown', (e) => {

    isDragging = true;

    startX = e.clientX;
    startY = e.clientY;

    spaceRoom.style.cursor = 'grabbing';
});

document.addEventListener('mousemove', (e) => {

    if (!isDragging) return;

    const dx = e.clientX - startX;
    const dy = e.clientY - startY;

    spaceMap.style.transform =
        `translate(${currentX + dx}px, ${currentY + dy}px)
        scale(${scale})`;
});

document.addEventListener('mouseup', (e) => {

    if (!isDragging) return;

    currentX += e.clientX - startX;
    currentY += e.clientY - startY;

    isDragging = false;

    spaceRoom.style.cursor = 'grab';

    checkResetButton();
});

spaceRoom.addEventListener('wheel', (e) => {

    e.preventDefault();

    const rect = spaceRoom.getBoundingClientRect();

    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const oldScale = scale;

    scale -= e.deltaY * 0.001;

    scale = Math.max(
        0.5,
        Math.min(scale, 3)
    );

    const scaleRatio = scale / oldScale;

    currentX =
        mouseX -
        (mouseX - currentX) * scaleRatio;

    currentY =
        mouseY -
        (mouseY - currentY) * scaleRatio;

    spaceMap.style.transform =
        `translate(${currentX}px, ${currentY}px)
        scale(${scale})`;

    checkResetButton();
});

function checkResetButton() {

    const movedDistance = Math.sqrt(
        Math.pow(currentX - HOME_X, 2)
        +
        Math.pow(currentY - HOME_Y, 2)
    );

    const scaleChanged =
        Math.abs(scale - HOME_SCALE);

    if (
        movedDistance > 80 ||
        scaleChanged > 0.2
    ) {
        resetViewBtn.classList.add('show');
    } else {
        resetViewBtn.classList.remove('show');
    }
}

resetViewBtn.addEventListener('click', () => {

    currentX = HOME_X;
    currentY = HOME_Y;
    scale = HOME_SCALE;

    spaceMap.style.transform =
        `translate(${currentX}px, ${currentY}px)
        scale(${scale})`;

    resetViewBtn.classList.remove('show');

});
