document.addEventListener("DOMContentLoaded", () => {
    console.log("heluaa")


    const code = document.getElementsByName("gamecode")[0].value
    console.log(code)

    window.setInterval(() => {
        let state = document.getElementsByName("status")[0].value
        if (state === "preparation"){
            console.log("preparation mode")
            checkstart(code)
        } else if (state === "init"){
            init()
        } else {
            console.log("play mode")
            fetchquestion(code)
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
        let { current_question, question_no } = result
        console.log(current_question)
        console.log(question_no)
        document.getElementById("question").innerHTML = current_question.question
        document.getElementById("option1").innerHTML = current_question.choice1
        document.getElementById("option2").innerHTML = current_question.choice2
        document.getElementById("option3").innerHTML = current_question.choice3
        document.getElementById("option4").innerHTML = current_question.choice4
    })
}



