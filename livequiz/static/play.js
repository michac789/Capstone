document.addEventListener("DOMContentLoaded", () => {
    console.log("heluaa")


    const code = document.getElementsByName("gamecode")[0].value
    console.log(code)

    // player button functionality
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

    // admin button functionality
    document.querySelector("#start").onclick = () => {start(code)}
    document.querySelector("#close").onclick = () => {close(code)}
    document.querySelector("#next").onclick = () => {next(code)}

    window.setInterval(() => {
        let state = document.getElementsByName("status")[0].value
        if (state === "preparation") {
            console.log("preparation mode")
            checkstart(code)
        } else if (state === "init") {
            init()
        } else if (state === "play") {
            console.log("play mode")
            fetchquestion(code)
        } else if (state === "closed") {
            console.log("closed")
            closequestion(code)
        } else {
            console.log("answered")
        }
    }, 1000)
})




function checkstart(code) {
    fetch(`/api/retrieve/${code}`, {
        method: "GET",
    })
    .then(response => response.json())
    .then(result => {
        if (result.started === true){
            document.getElementById("playzone").innerHTML = "Started"
            document.getElementsByName("status")[0].value = "init"
        } else {
            console.log("waiting for game to be started...")
        }
    })
}

function init() {
    let div = document.createElement("div")
    div.innerHTML = "question"
    div.setAttribute("id", "question")

    let option1 = document.createElement("button")
    option1.innerHTML = "content1"
    option1.setAttribute("id", "option1")
    option1.setAttribute("class", "options")

    let option2 = document.createElement("button")
    option2.innerHTML = "content2"
    option2.setAttribute("id", "option2")
    option2.setAttribute("class", "options")

    let option3 = document.createElement("button")
    option3.innerHTML = "content3"
    option3.setAttribute("id", "option3")
    option3.setAttribute("class", "options")

    let option4 = document.createElement("button")
    option4.innerHTML = "content4"
    option4.setAttribute("id", "option4")
    option4.setAttribute("class", "options")
    
    const wrapdiv = document.createElement("div")
    wrapdiv.append(div, option1, option2, option3, option4)
    document.getElementById("playzone").innerHTML = wrapdiv.innerHTML

    document.getElementsByName("status")[0].value = "play"
}

function fetchquestion(code) {
    fetch(`/api/retrieve/${code}`, {
        method: "VIEW",
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        let { current_question, question_no, open } = result
        document.getElementById("question").innerHTML = current_question.question
        document.getElementById("option1").innerHTML = current_question.choice1
        document.getElementById("option2").innerHTML = current_question.choice2
        document.getElementById("option3").innerHTML = current_question.choice3
        document.getElementById("option4").innerHTML = current_question.choice4
        if (open === false) {
            document.getElementsByName("status")[0].value = "closed"
        }
    })
}

function start(code) {
    fetch(`/api/action/${code}`, { method: "START",})
    .then(response => response.json())
    .then(result => { console.log(result) })
}

function close(code) {
    fetch(`/api/action/${code}`, { method: "CLOSE",})
    .then(response => response.json())
    .then(result => { console.log(result) })
}

function next(code) {
    fetch(`/api/action/${code}`, { method: "NEXT",})
    .then(response => response.json())
    .then(result => { console.log(result) })
}

function closequestion(code) {
    console.log("question closed")
    fetch(`/api/retrieve/${code}`, {
        method: "VIEW",
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        document.getElementById("playzone").innerHTML = `<h2>Closed</h2>`
        let { current_question, question_no, open } = result
        if (open === true) {
            document.getElementsByName("status")[0].value = "init"
        }
    })
}

function answer(code, ans) {
    console.log("submitting ans...")
    fetch(`/api/retrieve/${code}`, {
        method: "POST",
        body: JSON.stringify({ answer: ans,})
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        document.getElementsByName("status")[0].value = "answered"
    })
}



