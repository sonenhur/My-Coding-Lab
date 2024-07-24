const cardsArray = [
    { name: 'apple', img: 'images/apple.png' },
    { name: 'cherry', img: 'images/cherry.png' },
    { name: 'grape', img: 'images/grape.png' },
    { name: 'lemon', img: 'images/lemon.png' },
    { name: 'orange', img: 'images/orange.png' },
    { name: 'pear', img: 'images/pear.png' },
    { name: 'strawberry', img: 'images/strawberry.png' },
    { name: 'watermelon', img: 'images/watermelon.png' }
];

const gameGrid = cardsArray.concat(cardsArray).sort(() => 0.5 - Math.random());
const memoryGame = document.getElementById('memoryGame');
let firstGuess = '';
let secondGuess = '';
let count = 0;
let previousTarget = null;
let delay = 1200;

function createBoard() {
    gameGrid.forEach(item => {
        const card = document.createElement('div');
        card.classList.add('memory-card');
        card.dataset.name = item.name;

        const front = document.createElement('img');
        front.src = item.img;
        card.appendChild(front);

        memoryGame.appendChild(card);
    });
}

function resetGuesses() {
    firstGuess = '';
    secondGuess = '';
    count = 0;
    previousTarget = null;

    const selectedCards = document.querySelectorAll('.selected');
    selectedCards.forEach(card => {
        card.classList.remove('selected');
        card.classList.remove('flipped');
    });
}

function match() {
    const matchedCards = document.querySelectorAll('.selected');
    matchedCards.forEach(card => {
        card.classList.add('match');
    });
}

memoryGame.addEventListener('click', event => {
    const clicked = event.target;

    if (
        clicked.nodeName === 'DIV' ||
        clicked === previousTarget ||
        clicked.parentNode.classList.contains('flipped') ||
        clicked.parentNode.classList.contains('selected')
    ) {
        return;
    }

    if (count < 2) {
        count++;
        if (count === 1) {
            firstGuess = clicked.parentNode.dataset.name;
            clicked.parentNode.classList.add('selected');
            clicked.parentNode.classList.add('flipped');
        } else {
            secondGuess = clicked.parentNode.dataset.name;
            clicked.parentNode.classList.add('selected');
            clicked.parentNode.classList.add('flipped');
        }

        if (firstGuess && secondGuess) {
            if (firstGuess === secondGuess) {
                setTimeout(match, delay);
            }
            setTimeout(resetGuesses, delay);
        }
        previousTarget = clicked;
    }
});

const restartButton = document.getElementById('restartButton');
restartButton.addEventListener('click', () => {
    memoryGame.innerHTML = '';
    createBoard();
});

createBoard();
