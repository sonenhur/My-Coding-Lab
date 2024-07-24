const cardData = [
    ["Genshin_Impact_Official_Chibi_001", "images/Genshin_Impact_Official_Chibi_001.png"],
    // ["Genshin_Impact_Official_Chibi_002", "images/Genshin_Impact_Official_Chibi_002.png"],
    // ["Genshin_Impact_Official_Chibi_003", "images/Genshin_Impact_Official_Chibi_003.png"],
    ["Genshin_Impact_Official_Chibi_004", "images/Genshin_Impact_Official_Chibi_004.png"],
    // ["Genshin_Impact_Official_Chibi_005", "images/Genshin_Impact_Official_Chibi_005.png"],
    ["Genshin_Impact_Official_Chibi_006", "images/Genshin_Impact_Official_Chibi_006.png"],
    // ["Genshin_Impact_Official_Chibi_007", "images/Genshin_Impact_Official_Chibi_007.png"],
    ["Genshin_Impact_Official_Chibi_008", "images/Genshin_Impact_Official_Chibi_008.png"],
    // ["Genshin_Impact_Official_Chibi_009", "images/Genshin_Impact_Official_Chibi_009.png"],
    // ["Genshin_Impact_Official_Chibi_010", "images/Genshin_Impact_Official_Chibi_010.png"],
    // ["Genshin_Impact_Official_Chibi_058", "images/Genshin_Impact_Official_Chibi_058.png"],
    ["Genshin_Impact_Official_Chibi_061", "images/Genshin_Impact_Official_Chibi_061.png"],
    // ["Genshin_Impact_Official_Chibi_062", "images/Genshin_Impact_Official_Chibi_062.png"],
    // ["Genshin_Impact_Official_Chibi_063", "images/Genshin_Impact_Official_Chibi_063.png"],
    ["Genshin_Impact_Official_Chibi_065", "images/Genshin_Impact_Official_Chibi_065.png"],
    ["Genshin_Impact_Official_Chibi_080", "images/Genshin_Impact_Official_Chibi_080.png"],
    // ["Genshin_Impact_Official_Chibi_081", "images/Genshin_Impact_Official_Chibi_081.png"],
    // ["Genshin_Impact_Official_Chibi_082", "images/Genshin_Impact_Official_Chibi_082.png"],
    ["Genshin_Impact_Official_Chibi_084", "images/Genshin_Impact_Official_Chibi_084.png"],
    // ["Genshin_Impact_Official_Chibi_085", "images/Genshin_Impact_Official_Chibi_085.png"],
    ["Genshin_Impact_Official_Chibi_001", "images/Genshin_Impact_Official_Chibi_001.png"],
    // ["Genshin_Impact_Official_Chibi_002", "images/Genshin_Impact_Official_Chibi_002.png"],
    // ["Genshin_Impact_Official_Chibi_003", "images/Genshin_Impact_Official_Chibi_003.png"],
    ["Genshin_Impact_Official_Chibi_004", "images/Genshin_Impact_Official_Chibi_004.png"],
    // ["Genshin_Impact_Official_Chibi_005", "images/Genshin_Impact_Official_Chibi_005.png"],
    ["Genshin_Impact_Official_Chibi_006", "images/Genshin_Impact_Official_Chibi_006.png"],
    // ["Genshin_Impact_Official_Chibi_007", "images/Genshin_Impact_Official_Chibi_007.png"],
    ["Genshin_Impact_Official_Chibi_008", "images/Genshin_Impact_Official_Chibi_008.png"],
    // ["Genshin_Impact_Official_Chibi_009", "images/Genshin_Impact_Official_Chibi_009.png"],
    // ["Genshin_Impact_Official_Chibi_010", "images/Genshin_Impact_Official_Chibi_010.png"],
    // ["Genshin_Impact_Official_Chibi_058", "images/Genshin_Impact_Official_Chibi_058.png"],
    ["Genshin_Impact_Official_Chibi_061", "images/Genshin_Impact_Official_Chibi_061.png"],
    // ["Genshin_Impact_Official_Chibi_062", "images/Genshin_Impact_Official_Chibi_062.png"],
    // ["Genshin_Impact_Official_Chibi_063", "images/Genshin_Impact_Official_Chibi_063.png"],
    ["Genshin_Impact_Official_Chibi_065", "images/Genshin_Impact_Official_Chibi_065.png"],
    ["Genshin_Impact_Official_Chibi_080", "images/Genshin_Impact_Official_Chibi_080.png"],
    // ["Genshin_Impact_Official_Chibi_081", "images/Genshin_Impact_Official_Chibi_081.png"],
    // ["Genshin_Impact_Official_Chibi_082", "images/Genshin_Impact_Official_Chibi_082.png"],
    ["Genshin_Impact_Official_Chibi_084", "images/Genshin_Impact_Official_Chibi_084.png"],
    // ["Genshin_Impact_Official_Chibi_085", "images/Genshin_Impact_Official_Chibi_085.png"],
];

let flippedCards = [];
let lockBoard = false;
let startTime;
let timerInterval;

document.getElementById('startButton').addEventListener('click', startGame);

function adjustCardSize() {
    const cardSize = Math.min(window.innerWidth / 4, 120); // 화면 너비에 따라 카드 크기 조정
    document.querySelectorAll('.card').forEach(card => {
        card.style.width = `${cardSize}px`;
        card.style.paddingBottom = `${cardSize}px`; // 비율 유지
    });
}

window.addEventListener('resize', adjustCardSize);
document.addEventListener('DOMContentLoaded', adjustCardSize);

function startGame() {
    document.getElementById('record').classList.add('hidden');
    document.getElementById('startButton').disabled = true;
    startTime = new Date();
    timerInterval = setInterval(updateTimer, 1000);
    buildGameBoard(cardData);
    // 카드를 5초 동안 보여주기 위한 함수 호출
    showCardsForFiveSeconds();
}

function showCardsForFiveSeconds() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => card.classList.add('flipped')); // 카드 보이기

    countdownTimeout = setTimeout(() => {
        cards.forEach(card => card.classList.remove('flipped')); // 카드 숨기기
        startTimer(); // 타이머 시작
    }, 5000); // 5초 후에 카드 숨기기
}

function startTimer() {
    startTime = new Date();
    timerInterval = setInterval(updateTimer, 1000);
}

function updateTimer() {
    const elapsedTime = Math.floor((new Date() - startTime) / 1000);
    const minutes = String(Math.floor(elapsedTime / 60)).padStart(2, '0');
    const seconds = String(elapsedTime % 60).padStart(2, '0');
    document.getElementById('timer').textContent = `Time: ${minutes}:${seconds}`;
}

function endGame() {
    clearInterval(timerInterval);
    document.getElementById('startButton').disabled = false;
    const finalTime = document.getElementById('timer').textContent;
    document.getElementById('record').textContent = `축하합니다! 당신의 기록은: ${finalTime}`;
    document.getElementById('record').classList.remove('hidden');
}

function flipCard(card) {
    if (lockBoard || card.classList.contains('flipped') || card.classList.contains('matched')) return;

    card.classList.add('flipped');
    flippedCards.push(card);

    if (flippedCards.length === 2) {
        lockBoard = true; // 보드 잠금
        setTimeout(() => {
            checkMatch(flippedCards);
            flippedCards = [];
            if (document.querySelectorAll('.matched').length === cardData.length) {
                endGame(); // 게임 종료 시 기록 표시
            }
            lockBoard = false; // 보드 잠금 해제
        }, 500); // 카드 뒤집기 지연 시간
    }
}

function unflipCard(card) {
    card.classList.remove('flipped');
}

function checkMatch(cards) {
    if (cards[0].dataset.name === cards[1].dataset.name) {
        cards.forEach(card => card.classList.add('matched'));
    } else {
        cards.forEach(card => setTimeout(() => unflipCard(card), 500)); // 카드가 다시 뒤집히는 시간
    }
}

function createCard(data) {
    const card = document.createElement('div');
    card.classList.add('card');
    card.dataset.name = data[0];
    const img = document.createElement('img');
    img.src = data[1];
    img.alt = data[0];
    const back = document.createElement('div');
    back.classList.add('back');
    back.textContent = '?';
    card.appendChild(img);
    card.appendChild(back);
    card.addEventListener('click', () => flipCard(card));
    return card;
}

function buildGameBoard(data) {
    const board = document.getElementById('gameBoard');
    board.innerHTML = ''; // 게임 보드 초기화
    data.sort(() => Math.random() - 0.5);
    data.forEach(item => {
        board.appendChild(createCard(item));
    });
}