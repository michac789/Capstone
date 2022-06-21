function create(el, attr, inner=null) {
    let new_el = document.createElement(el)
    for(let key in attr) {
        new_el.setAttribute(key, attr[key])
    }
    if (inner != null) {
        new_el.innerHTML = `${inner}`
    }
    return new_el
}

function creappend(el, attr, args) {
    let new_el = document.createElement(el)
    for(let key in attr) {
        new_el.setAttribute(key, attr[key])
    }
    args.forEach(arg => new_el.append(arg))
    return new_el
}

function radioinputs(name, options) {
    let new_el = create("div", {})
    options.forEach(op => {
        new_el.append(creappend("div", {},
            [create("input", {
                "type": "radio", "name": name, "id": op.id, "value": op.val
            }), create("label", { "for": op.id }, op.val)]
        ))
    })
    return new_el
}

export { create, creappend, radioinputs }
