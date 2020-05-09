
$(function () {
    const $formEvents = $("#form-events");
    const $formPlaceBet = $("#form-placebet");

    $formPlaceBet.on('submit', function (e) {
        e.preventDefault();

        let json = {
            "info": getFormData($formPlaceBet),
            "events": $formEvents.serializeArray()
        };

        placeBet(json)
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
                // location.reload()
            },
            error: function (errMsg) {
                showMessage(errMsg['responseJSON']['message'], "danger");
            }
        })
    }

    function getFormData($form) {
        let unindexed_array = $form.serializeArray();
        let indexed_array = {};

        $.map(unindexed_array, function (n, i) {
            indexed_array[n['name']] = n['value'];
        });

        return indexed_array;
    }

    function clearAll() {
        $formEvents.find('input').prop("checked", false);
    }
});