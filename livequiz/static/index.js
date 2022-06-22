document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".deletesession").forEach(
        el => el.onclick = (e) => {
            deletesession(e.target.dataset.id)
        }
    )
})

function deletesession(id) {

}
