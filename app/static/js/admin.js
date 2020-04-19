$(function () {
    $('.event-outcome-select').on('change', function () {
        let outcome_id = this.value;
        if (outcome_id === '')
            return;

        let event_id = $(this).attr("name");

        $.ajax({
            type: "POST",
            url: `/admin/event/${event_id}/update_outcome`,
            data: JSON.stringify({"outcome_id": outcome_id}),
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
    })
});