const cardData = [
    ["apple", "images/apple.png"],
    ["cherry", "images/cherry.png"],
    ["grape", "images/grape.png"],
    ["lemon", "images/lemon.png"],
    ["orange", "images/orange.png"],
    ["peach", "images/peach.png"],
    ["strawberry", "images/strawberry.png"],
    ["watermelon", "images/watermelon.png"],
    ["apple", "images/apple.png"],
    ["cherry", "images/cherry.png"],
    ["grape", "images/grape.png"],
    ["lemon", "images/lemon.png"],
    ["orange", "images/orange.png"],
    ["peach", "images/peach.png"],
    ["strawberry", "images/strawberry.png"],
    ["watermelon", "images/watermelon.png"],
];

let flippedCards = [];
let lockBoard = false;
let startTime;
let timerInterval;

document.getElementById('startButton').addEventListener('click', startGame);

function startGame() {
    document.getElementById('record').classList.add('hidden');
    document.getElementById('startButton').disabled = true;
    startTime = new Date();
    timerInterval = setInterval(updateTimer, 1000);
    buildGameBoard(cardData);
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
