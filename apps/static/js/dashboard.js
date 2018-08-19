document.addEventListener("DOMContentLoaded", () => {
    let percent = document.querySelector("#progress").dataset.percent
    document.querySelector("#progress").style.width = `${percent}%`

    fetch("/revenue",{
        method: "GET",
    })
    .then( response=>response.json())
    .then(response =>{
        create_chart(response.revenue, response.previous)
    })


})


function create_chart(revenue, previous) {
    let year = new Date().getFullYear()
    let ctx = document.querySelector("#monthChart");

    let mychart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            datasets:[{
                label: `${year} Revenue`,
                data: revenue,
                // backgroundColor: "green",
                borderColor: "blue",
                fill: false
            },
            {
                label: `${year-1} Revenue`,
                data: previous,
                // backgroundColor: "green",
                borderColor: "orange",
                fill: false
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    })
}