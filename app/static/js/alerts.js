function showMessage(message, category = "info") {
    const $alert = $(`<div class="alert fade in alert-dismissible show alert-${category}">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true" style="font-size:20px">×</span>
                </button>
                ${message}
            </div>`);

    $(".flashes-container").append($alert);

    setTimeout(function () {
        $alert.fadeOut();
    }, 10000);
}