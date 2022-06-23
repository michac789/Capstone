import { create, creappend } from './util.js'

document.addEventListener("DOMContentLoaded", () => {
    // get game session code
    const code = document.getElementsByName("gamecode")[0].value
    console.log(code)

    // player button functionality to choose the correct answer
    let playzone = document.querySelector("#playzone")
    playzone.onclick = (el) => {
        if (el.target && el.target.matches("#option1")) {
            console.log("o1")
            answer(code, 1)
        } else if (el.target && el.target.matches("#option2")) {
            console.log("o2")
            answer(code, 2)
        } else if (el.target && el.target.matches("#option3")) {
            console.log("o3")
            answer(code, 3)
        } else if (el.target && el.target.matches("#option4")) {
            console.log("o4")
            answer(code, 4)
        }
    }

    // periodically check and render components based on game state
    window.setInterval(() => {
        let state = document.getElementsByName("status")[0].value
        console.log(`current state: ${state}`)
        if (state === "prep") {
            console.log("state: prep")
            state_prep(code)
        } else if (state === "play") {
            console.log("play mode")
            state_play(code)
        } else if (state === "closed") {
            console.log("closed")
            state_closed(code)
        } else {
            console.log("answered")
            state_answered(code)
        }
    }, 1000)

    // TODO - before going to 'closed' state, automatically disable all buttons
    // TODO - handle end of question
})

// 'prep' state: check game state from the server, change to 'play' or 'closed' state
function state_prep(code) {
    fetch(`/api/retrieve/${code}`, { method: "GET",})
    .then(response => response.json())
    .then(result => {
        console.log(result)
        if (result.status === "prep") {
            document.getElementById("message").innerHTML = "Waiting host to start game..."
        } else if (result.status === "play") {
            document.getElementById("message").innerHTML = "Game is starting... loading..."
            init()
            render_question(code)
            document.getElementsByName("status")[0].value = "play"
        } else if (result.status === "closed") {
            init()
            document.getElementsByName("status")[0].value = "closed"
        }
    }).catch(error => console.log(error))
}

// render DOM components first before switching from 'prep' state to 'play'/'closed' state
function init() {
    document.getElementById("playzone").innerHTML = creappend("div", {}, [
        create("div", { "id": "question",}, "loading question..."),
        create("button", { "id": "option1", "class": "options",}, "loading..."),
        create("button", { "id": "option2", "class": "options",}, "loading..."),
        create("button", { "id": "option3", "class": "options",}, "loading..."),
        create("button", { "id": "option4", "class": "options",}, "loading..."),
    ]).innerHTML
}

// render questions after calling init when switching to play state
function render_question(code) {
    fetch(`/api/retrieve/${code}`, { method: "VIEW",})
    .then(response => response.json())
    .then(result => {
        console.log(result)
        const { current_question, question_no } = result
        document.getElementById("question").innerHTML = current_question.question
        document.getElementById("option1").innerHTML = current_question.choice1
        document.getElementById("option2").innerHTML = current_question.choice2
        document.getElementById("option3").innerHTML = current_question.choice3
        document.getElementById("option4").innerHTML = current_question.choice4
    })
    document.getElementById("message").innerHTML = "Answer before the question is closed..."
}

// 'play' state: remains in this state until either question is closed or answered
function state_play(code) {
    fetch(`/api/retrieve/${code}`, { method: "GET",})
    .then(response => response.json())
    .then(result => {
        console.log(result)
        if (result.status === "prep") {
            document.getElementsByName("status")[0].value = "prep"
        } else if (result.status === "play") {
            console.log("...")
        } else if (result.status === "closed") {
            document.getElementsByName("status")[0].value = "closed"
        }
    }).catch(error => console.log(error))
}

// 'answered' state: remain in this state until question closed
function state_answered(code) {
    fetch(`/api/retrieve/${code}`, { method: "GET",})
    .then(response => response.json())
    .then(result => {
        console.log(result)
        if (result.status === "prep") {
            document.getElementsByName("status")[0].value = "prep"
        } else if (result.status === "play") {
            console.log("...waiting until question is closed...")
        } else if (result.status === "closed") {
            document.getElementsByName("status")[0].value = "closed"
        }
    }).catch(error => console.log(error))
}

// 'closed' state: remains in this state until next question
function state_closed(code) {
    console.log("question closed")
    fetch(`/api/retrieve/${code}`, { method: "GET",})
    .then(response => response.json())
    .then(result => {
        console.log(result)
        document.getElementById("message").innerHTML = `<h2>Closed</h2>`
        if (result.status == "play") {
            document.getElementsByName("status")[0].value = "prep"
        }
    }).catch(error => console.log(error))
}

// api call to register participants' answer, change to 'answered' state if successful
function answer(code, ans) {
    console.log("submitting ans...")
    fetch(`/api/retrieve/${code}`, {
        method: "POST",
        body: JSON.stringify({ answer: ans,})
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        if (result.message == "closed") {
            document.getElementsByName("status")[0].value = "closed"
        }
        document.getElementsByName("status")[0].value = "answered"
        document.getElementById("message").innerHTML =
            `you answered option ${result.answer}, waiting for next question`
    }).catch(error => console.log(error))
}
