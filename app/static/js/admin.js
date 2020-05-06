$(function () {
    $('#save-outcomes-btn').on('click', function (event) {
        event.preventDefault();
        let json_out = $('.event-outcome-select').serializeArray().map(elem => {
            return {'event_id': elem['name'], 'outcome_id': elem['value']}
        });
        console.log();
        $.ajax({
            type: "POST",
            url: window.location.href.split("/").pop()+"/update_outcome",
            data: JSON.stringify(json_out),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                showAlert(data['message'], "success");
                // location.reload()
            },
            error: function (errMsg) {
                showAlert(errMsg['responseJSON']['message'], "danger");
            }

        })
    });
});