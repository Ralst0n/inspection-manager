document.addEventListener("DOMContentLoaded", () => {
    let percent = document.querySelector("#progress").dataset.percent
    document.querySelector("#progress").style.width = `${percent}%`
})