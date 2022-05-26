function millisToMinutesAndSeconds(millis) {
    var minutes = Math.floor(millis / 60000);
    var seconds = ((millis % 60000) / 1000).toFixed(0);
    return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
}
document.getElementById("leaderboardtable").hidden = true;
var today = new Date();
var year = today.getFullYear();
var mes = today.getMonth() + 1;
var dia = today.getDate();
var todayDate = year + "-" + (mes < 10 ? '0' : '') + mes + "-" + (dia < 10 ? '0' : '') + dia;
console.log(todayDate);
var start = new Date();
var runTime = start;
const displayTile = document.querySelector('.tile-container');
const keyboard = document.querySelector('.key-container');
let res = document.getElementById('succ');
let hid = document.getElementById('hid');
res.innerHTML = "Please wait for the game to load";
var response = "";
const popup = document.querySelector('.popupBoxInit');
const close = document.querySelector('.close');
window.onload = function () {
    setTimeout(function () {
        popup.style.display = "block";
    }, 0)
}

close.addEventListener('click', () => {
    popup.style.display = "none";
})


const options1 = {
    method: 'GET',
    headers: {
        'X-RapidAPI-Host': options1_host,
        'X-RapidAPI-Key': options1_key
    }
};

const options2 = {
    method: 'GET',
    headers: {
        'X-RapidAPI-Host': options2_host,
        'X-RapidAPI-Key': options2_key
    }
};


function getvals() {
    return fetch('https://random-words5.p.rapidapi.com/getMultipleRandom?count=5', options2)
        .then((response) => response.json())
        .then((responseData) => {
            var wo = responseData[1];
            console.log(wo);
            return wo;
        })
        .catch(error => console.warn(error));
}


// function getvals() {
//     return fetch('https://random-word-api.herokuapp.com/word')
//         .then((response) => response.json())
//         .then((responseData) => {
//             var wo = responseData;
//             return wo;
//         })
//         .catch(error => console.warn(error));
// }



// function getvals() {
//     return fetch('https://word-of-the-day2.p.rapidapi.com/word/dc', options1)
//         .then((response) => response.json())
//         .then((responseData) => {
//             var word = responseData[0]["word"]
//             var wordl = word.split(' ');
//             return wordl[0];
//         })
//         .catch(error => console.warn(error));
// }

getvals().then(response => {
    var rowGuess;
    response = response.toUpperCase();
    res.innerHTML = "Start game";
    hid.innerHTML = "Guess the hidden word";
    var size = response.length;

    rowGuess = Array(size).fill().map(() => Array(size).fill());
    let currentRow = 0;
    let currentTile = 0;
    let gameOverBool = false;

    rowGuess.forEach((rowGuess, rowGuessIndex) => {
        const rowElement = document.createElement('div');
        rowElement.setAttribute('id', 'rowGuess_' + rowGuessIndex);
        rowGuess.forEach((_guess, guessIndex) => {
            const tileElement = document.createElement('div');
            tileElement.setAttribute('id', 'rowGuess_' + rowGuessIndex + '_tile_' + guessIndex);
            tileElement.classList.add('tile');
            rowElement.append(tileElement);
        })
        displayTile.append(rowElement);
    })


    const keys = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
        'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'ENTER', 'DEL'];

    keys.forEach(key => {
        const buttonElement = document.createElement('button');
        buttonElement.textContent = key;
        buttonElement.setAttribute('id', key);
        buttonElement.addEventListener('click', () => keyFunctionality(key));
        keyboard.append(buttonElement);

    })

    // var link = document.getElementById("A");
    // link.onclick= function() {alert('clicked');};
    // if(link.addEventListener){
    //     link.addEventListener('click', function(){
    //        alert('clicked');
    //     });
    //  }else if(link.attachEvent){
    //     link.addEventListener('onclick', function(){
    //        alert('clicked');
    //     });
    // }

    const keyFunctionality = (letter) => {
        if (!gameOverBool) {
            if (letter === 'DEL') {
                deleteLetter();
                return;
            }
            if (letter === 'ENTER') {
                checkRow();
                return;
            }
            addLetter(letter);
        }
    }

    function key_id(i) {
        var keybid = document.getElementById(Array.find(input));

    }

    const addLetter = (letter) => {
        if (currentTile < size && currentRow < size + 1) {
            const tile = document.getElementById('rowGuess_' + currentRow + '_tile_' + currentTile);
            tile.textContent = letter;
            rowGuess[currentRow][currentTile] = letter;
            tile.setAttribute('data', letter);
            currentTile++;
        }
    }

    const deleteLetter = () => {
        if (currentTile > 0) {
            currentTile--;
            const tile = document.getElementById('rowGuess_' + currentRow + '_tile_' + currentTile);
            tile.textContent = '';
            rowGuess[currentRow][currentTile] = '';
            tile.setAttribute('data', '');
        }
    }

    let guess_w = document.getElementById('guess');
    const checkRow = () => {
        const guess = rowGuess[currentRow].join('')
        if (guess === response) {
            console.log("super success");
        }
        if (currentTile > size - 1) {
            var guess_obj = guess.toLowerCase();
            const options = {
                method: 'GET',
                headers: {
                    'X-RapidAPI-Host': options_host,
                    'X-RapidAPI-Key': options_key
                }
            };

            fetch('https://wordsapiv1.p.rapidapi.com/words/' + guess_obj + '/definitions', options)
                .then(response => response.json())
                .then(response => {
                    if (response['success'] === false) {
                        guess_w.innerHTML = guess_obj + " is not a valid word, Please try again";
                        return;
                    }
                })
                .catch(err => console.error(err));
            flipTile();
            if (response === guess) {
                let runTime = new Date() - start;
                timeTaken = (millisToMinutesAndSeconds(runTime));
                res.innerHTML = "Correct Word";
                // leadb.hidden;
                hid.innerHTML = "Hidden word is " + response;
                document.getElementById("leaderboardtable").hidden = false;
                guess_w.innerHTML = "";
                gameOverBool = true;
                displayTile.style.display = "none";
                addLeaderboardval();
                return
            }
            else {
                if (currentRow >= size - 1) {
                    gameOverBool = true;
                    res.innerHTML = "Game Over, you Lose";
                    document.getElementById("leaderboardtable").hidden = false;
                    hid.innerHTML = "Hidden word is " + response;
                    guess_w.innerHTML = "You guessed " + guess_obj;
                    displayTile.style.display = "none";
                    return
                }
                if (currentRow < size) {
                    currentRow++;
                    currentTile = 0;
                    guess_w.innerHTML = "You guessed " + guess_obj;
                }
            }
        }
    }


    const addColorToKey = (keyLetter, color) => {
        const key = document.getElementById(keyLetter);
        key.classList.add(color);
    }

    const flipTile = () => {
        const rowTiles = document.querySelector('#rowGuess_' + currentRow).childNodes;
        let guess_check = response;
        const guess = [];

        rowTiles.forEach(tile => {
            guess.push({ letter: tile.getAttribute('data'), color: 'grey-overlay' });
        })

        guess.forEach((guess, index) => {
            if (guess.letter === response[index]) {
                guess.color = 'green-overlay';
                guess_check = guess_check.replace(guess.letter, '');
            }
        })
        guess.forEach(guess => {
            if (guess_check.includes(guess.letter)) {
                guess.color = 'yellow-overlay';
                guess_check = guess_check.replace(guess.letter, '')
            }
        })

        rowTiles.forEach((tile, index) => {
            setTimeout(() => {
                tile.classList.add('flip');
                tile.classList.add(guess[index].color);
                addColorToKey(guess[index].letter, guess[index].color);
            }, 500 * index);
        })
    }

    function addLeaderboardval() {
        data_d = { 'response': response, 'time': timeTaken, 'date': todayDate };
        jQuery.ajax({
            url: "/processleaderboard",
            data: data_d,
            type: "POST",
        });
    }
});

function leaderboard() {
    data_d = {};
    jQuery.ajax({
        url: "/leaderboard",
        data: data_d,
        type: "POST",

    });
    window.location.href = "/leaderboard.html";
}

