document.addEventListener("DOMContentLoaded", () => {
    // get game session code
    const code = document.getElementsByName("gamecode")[0].value

    // admin button functionality
    adminbuttonvisibility(true, false, false)
    document.querySelector("#start").onclick = () => { start(code) }
    document.querySelector("#close").onclick = () => { close(code) }
    document.querySelector("#next").onclick = () => { next(code) }
})

// function to control admin buttons
function adminbuttonvisibility(start, close, next) {
    document.querySelector("#start").style.display = start == true ? "block" : "none"
    document.querySelector("#close").style.display = close == true ? "block" : "none"
    document.querySelector("#next").style.display = next == true ? "block" : "none"
}

// api call to start the game
function start(code) {
    fetch(`/api/action/${code}`, { method: "START",})
    .then(response => response.json())
    .then(_ => { adminbuttonvisibility(false, true, false)}
    ).catch(error => console.log(error))
}

// api call to close a particular question
function close(code) {
    fetch(`/api/action/${code}`, { method: "CLOSE",})
    .then(response => response.json())
    .then(_ => { adminbuttonvisibility(false, false, true) }
    ).catch(error => console.log(error))
}

// api call to move to next question
function next(code) {
    fetch(`/api/action/${code}`, { method: "NEXT",})
    .then(response => response.json())
    .then(_ => { adminbuttonvisibility(false, true, false) }
    ).catch(error => console.log(error))
}
