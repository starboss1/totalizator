
$(function () {
    const $formEvents = $("#form-events");
    const $formPlaceBet = $("#form-placebet");

    $formPlaceBet.on('submit', function (e) {
        e.preventDefault();

        let json = {
            "info": getFormData($formPlaceBet),
            "events": $formEvents.serializeArray()
        };

        if(json.events.length > 0) {
            placeBet(json);
        }
        else
            showMessage("Select one or more events", "danger")
    });

    $(".js-parlay-clear").click(function () {
        clearAll();
    });

    function placeBet(json) {
        $.ajax({
            type: "POST",
            url: "/play/placebet",
            data: JSON.stringify(json),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                showMessage(data['message'], "success");
                $formEvents[0].reset();
                $formPlaceBet[0].reset();
            },
            error: function (errMsg) {
                showMessage(errMsg['responseJSON']['message'], "danger");
            }
        })
    }

    function getFormData($form) {
        let array_unind = $form.serializeArray();
        let array_ind = {};

        $.map(array_unind, function (n, i) {
            array_ind[n['name']] = n['value'];
        });

        return array_ind;
    }

    function clearAll() {
        $formEvents.find('input').prop("checked", false);
    }
});