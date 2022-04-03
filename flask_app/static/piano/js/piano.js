const keys = document.querySelectorAll('.key');
const whiteKeys = document.querySelectorAll('.key.white');
const blackKeys = document.querySelectorAll('.key.black');
const creepy = document.getElementById('end');
document.querySelector(".awkownimage").style.opacity = 0;
const whites = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'];
const blacks = ['w', 'e', 't', 'y', 'u', 'o', 'p']
let str = "weseeyo";
let findstr = "";
// Here we are using the button to play the sound
keys.forEach(key => {
    key.addEventListener('click', () => playNote(key))
})


document.addEventListener('keydown', ke => {
    if (ke.repeat) return
    const key = ke.key
    const whiteKeyIndex = whites.indexOf(key)
    const blackKeyIndex = blacks.indexOf(key)
    if (blackKeyIndex >= 0) {
        playNote(blackKeys[blackKeyIndex])
        findstr += key;
    }

    if (whiteKeyIndex >= 0) {
        playNote(whiteKeys[whiteKeyIndex])
        findstr += key;
    }
    

})
// Here the code will change the key button when pressed
let playNote = (key) => {
    const noteSound = document.getElementById(key.dataset.note)
    noteSound.currentTime = 0
    noteSound.play()


    key.classList.add('active')
    noteSound.addEventListener('ended', () => {
        key.classList.remove('active')
    })


    // awekens appear here

    if (findstr === str) {
        document.querySelector(".awkownimage").style.opacity = 1;
        document.getElementById("piano-text").innerHTML = "I have awoken";
        creepy.play();

        keys.forEach(key => {
            key.removeEventListener('click', () => playNote(key))
        })
        
    }

}


