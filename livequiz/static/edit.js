import { create, creappend, radioinputs } from './util.js'

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".questiondiv").forEach(
        el => el.onclick = (e) => {
            if (e.target && e.target.matches(".editbutton")) {
                edit(e.target.dataset.quesid)
            }
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
    return creappend("div", {}, [label, input])
}

function edit(id) {
    const ques = creappend("div", {}, [
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
    const ans = creappend("div", {}, [
        create("section", {}, "Correct Answer: "),
        radioinputs(`${id}_ans`, [
            {"id": `${id}_1`, "val": "Option 1"},
            {"id": `${id}_2`, "val": "Option 2"},
            {"id": `${id}_3`, "val": "Option 3"},
            {"id": `${id}_4`, "val": "Option 4"},
    ])])
    const button = create("button", {
        "class": "savebutton", "data-id": `${id}`, "onclick": ``,},
        "Save Changes")
    document.querySelector(`.questiondiv[data-quesid='${id}']>.questioneditable`).innerHTML =
        creappend("div", {}, [ques, opt1, opt2, opt3, opt4, ans, button]).innerHTML
}
