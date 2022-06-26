const create = (el, attr, inner=null) => {
    let new_el = document.createElement(el)
    for(let key in attr) {
        new_el.setAttribute(key, attr[key])
    }
    if (inner != null) {
        new_el.innerHTML = `${inner}`
    }
    return new_el
}

const creappend = (el, attr, args) => {
    let new_el = document.createElement(el)
    for(let key in attr) {
        new_el.setAttribute(key, attr[key])
    }
    args.forEach(arg => new_el.append(arg))
    return new_el
}

const capstonetitle = (arg) => {
    document.querySelector("#capstonetitle").innerHTML =
        creappend("div", {}, [
            create("li", { "class": "nav-item m-1",}, creappend("div", {}, [
                create(
                    "span", { "class": `capstonetitle ${arg}`,}, "Capstone"
                )
            ]).innerHTML)
        ]).innerHTML
}

const adjust_title = () => {
    if (window.innerWidth <= 769) {
        document.querySelector("#capstonetitle").innerHTML = ""
    } else if (window.innerWidth <= 999) {
        capstonetitle("")
    } else if (window.innerWidth <= 1299) {
        capstonetitle("largefont")
    } else {
        capstonetitle("superlargefont")
    }
}

document.addEventListener("DOMContentLoaded", () => {
    window.dispatchEvent(new Event('resize'));
    window.addEventListener('resize', () => {
        adjust_title()
    });
    adjust_title()
})
