category = document.querySelector("#category")
window.addEventListener("load", () => {
    handleRecommendation()
})
category.addEventListener("change", () => {
    handleRecommendation()
})

function handleRecommendation() {
    $.ajax({
        url: `${window.location.protocol}//${window.location.host}/api/get-recommendation/`,
        type: "get", //send it through get method
        data: {
            category_id: category.value,
        },
        success: function (response) {
            data = response[0]
            document.querySelector("#recommendation").innerHTML = `
                 <div class="card shadow mb-4">
                    <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-success">Рекомендация</h6>
                    </div>
                    <div class="card-body">

                        <h5 class="text-success font-weight-bold">${data.title}</h5>
                        <p>${data.preview_text.replaceAll("\n", "<br />")}</p>

                        <a class="btn btn-outline-success" href="#" data-toggle="modal" data-target="#recInfoModal">
                            Подробнее
                        </a>
                    </div>
                    <div class="card-footer">
                    <p class="m-0 p-0">Вы получите <span class="text-warning"><i class="fa-solid fa-star"></i> ${data.score}</span> баллов за кг!</p>
                    </div>
                </div>
                `
            document.querySelector("#rec-text").innerHTML = `
                       <div>
                            <img src="${data.image}" alt="${data.title}" class="w-100 mb-3">
                            <h5 class="text-success font-weight-bold">${data.title}</h5>
                            <p>${data.text.replaceAll("\n", "<br />")}</p>
                       </div>
                `
            document.querySelector("#rec-footer").innerHTML = `
                <p class="m-0 p-0">Вы получите <span class="text-warning"><i class="fa-solid fa-star"></i> ${data.score}</span> баллов за кг!</p>
                `
        },
        error: function (xhr) {
            console.log(xhr)
            document.querySelector("#recommendation").innerHTML = ''
        }
    });
}