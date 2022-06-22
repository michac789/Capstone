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
        let radbtn = create("input", {
            "type": "radio", "name": name, "id": op.id, "value": op.val,
        })
        if (op.checked === true) {
            radbtn.setAttribute("checked", "checked")
        }
        new_el.append(creappend("div", {},
            [radbtn, create("label", { "for": op.id }, op.val)]
        ))
    })
    return new_el
}

async function fetchURL(url, obj, strict=false) {
    let response = await fetch(url, obj)
    if (strict) {
        if (response.status == 200) {
            let json = await response.json()
            return json
        }
        throw new Error(response.status)
    } else {
        return response
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export { create, creappend, radioinputs, fetchURL, getCookie }
