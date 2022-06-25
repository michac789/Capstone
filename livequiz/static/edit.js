import { create, creappend, radioinputs, fetchURL, getCookie } from './util.js'

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".questiondiv").forEach(
        el => el.onclick = (e) => {
            if (e.target && e.target.matches(".editbutton")) {
                edit(e.target.dataset.quesid)
            }
            if (e.target && e.target.matches(".savebutton")) {
                save(e.target.dataset.quesid)
            }
        }
    )
    document.querySelectorAll(".deletebutton").forEach(
        el => el.onclick = (e) => {
            deletequestion(e.target.value)
        }
    )
})

function form_input(id, opt, lab) {
    const label = create("label", { "for": `${id}_${opt}`,}, lab)
    const input = create("input", { "type": "text", "id": `${id}_${opt}`, "name": opt,
        "value": document.querySelector(
            `.questiondiv[data-quesid='${id}']>.questioneditable>.${opt}`
        ).innerHTML
    })
    return creappend("div", { "class": opt,}, [label, input])
}

function edit(id) {
    const ques = creappend("div", { "class": "ques",}, [
        create("label", { "for": `${id}_ques`,}, "Question: "),
        create("input", { "type": "text", "id": `${id}_ques`, name: "ques",
            "value": document.querySelector(
                `.questiondiv[data-quesid='${id}']>.questioneditable>.ques`
            ).innerHTML})
    ])
    const opt1 = form_input(id, "opt1", "Option 1: ")
    const opt2 = form_input(id, "opt2", "Option 2: ")
    const opt3 = form_input(id, "opt3", "Option 3: ")
    const opt4 = form_input(id, "opt4", "Option 4: ")
    const chosen = document.querySelector(
            `.questiondiv[data-quesid='${id}']>.questioneditable>.ans`
        ).innerHTML
    const ans = creappend("div", { "class": "ans",}, [
        create("section", {}, "Correct Answer: "),
        radioinputs(`${id}_ans`, [
            {"id": `${id}_1`, "val": "Option 1", "checked": chosen === "1" ? true : false},
            {"id": `${id}_2`, "val": "Option 2", "checked": chosen === "2" ? true : false},
            {"id": `${id}_3`, "val": "Option 3", "checked": chosen === "3" ? true : false},
            {"id": `${id}_4`, "val": "Option 4", "checked": chosen === "4" ? true : false},
    ])])
    const button = create("button", {
        "class": "savebutton", "data-quesid": `${id}`,}, "Save Changes")
    document.querySelector(`.questiondiv[data-quesid='${id}']>.questioneditable`).innerHTML =
        creappend("div", {}, [ques, opt1, opt2, opt3, opt4, ans, button]).innerHTML
}

function save(id) {
    const getcontent = (id, arg) => {
        return `.questiondiv[data-quesid='${id}']>.questioneditable>.${arg}`
    }
    const getchecked = (id) => {
        let checked = 0
        document.querySelectorAll(`${getcontent(id, "ans")}>div>div>input`)
        .forEach((el, i) => { if (el.checked) { checked = i + 1 } })
        return checked
    }
    console.log(getchecked(id))
    fetchURL(`/api/savequestion/${id}`, {
            method: "PUT",
            body: JSON.stringify({
                ques: document.querySelector(`${getcontent(id, "ques")}>input`).value,
                opt1: document.querySelector(`${getcontent(id, "opt1")}>input`).value,
                opt2: document.querySelector(`${getcontent(id, "opt2")}>input`).value,
                opt3: document.querySelector(`${getcontent(id, "opt3")}>input`).value,
                opt4: document.querySelector(`${getcontent(id, "opt4")}>input`).value,
                ans: getchecked(id),
            }),
            headers: { "X-CSRFToken": getCookie('csrftoken'),},
        }
    ).then(response => response.json()
    ).then(res => {
        document.querySelector(`.questiondiv[data-quesid='${id}']>.questioneditable`).innerHTML =
        creappend("div", {}, [
            create("span", { "class": "ques_text",}, "Question: "),
            create("span", { "class": "ques",}, res.q.ques), create("br", {}),
            create("span", { "class": "opt1_text",}, "Option 1: "),
            create("span", { "class": "opt1",}, res.q.opt1), create("br", {}),
            create("span", { "class": "opt2_text",}, "Option 2: "),
            create("span", { "class": "opt2",}, res.q.opt2), create("br", {}),
            create("span", { "class": "opt3_text",}, "Option 3: "),
            create("span", { "class": "opt3",}, res.q.opt3), create("br", {}),
            create("span", { "class": "opt4_text",}, "Option 4: "),
            create("span", { "class": "opt4",}, res.q.opt4), create("br", {}),
            create("span", { "class": "ans_text",}, "Ans: "),
            create("span", { "class": "ans",}, res.q.ans), create("br", {}),
            create("button", { "class": "editbutton", "data-quesid": id,}, "Edit"),
        ]).innerHTML
    }).catch(error => console.log(error))
}

function deletequestion(id) {
    fetchURL(`/api/savequestion/${id}`, {
        method: "DELETE",
        body: JSON.stringify({}),
        headers: { "X-CSRFToken": getCookie('csrftoken'),},
    }).then(response => response.json()
    ).then(_ => {
        window.location.reload()
        //window.location.href = `http://${window.location.host}${window.location.pathname}?page=2`
        path.reload()
        document.querySelector(`.questiondiv[data-quesid='${id}']>.questioneditable`).innerHTML =
            "Question deleted, please click here to reload..."
    }).catch(error => console.log(error))
}
