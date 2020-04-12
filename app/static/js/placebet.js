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

    $(".js-parlay-random").click(function () {
        randomChoice();
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
                showAlert(data['message'], "success");
                $formEvents[0].reset();
                $formPlaceBet[0].reset();
                // location.reload()
            },
            error: function (errMsg) {
                showAlert(errMsg['responseJSON']['message'], "danger");
            }
        })
    }

    function getFormData($form) {
        var unindexed_array = $form.serializeArray();
        var indexed_array = {};

        $.map(unindexed_array, function (n, i) {
            indexed_array[n['name']] = n['value'];
        });

        return indexed_array;
    }

    function randomChoice() {
        $formEvents.find('.event-outcomes').each(function () {
            let $inputs = $(this).find("input");
            $($inputs[Math.floor(Math.random() * $inputs.length)]).prop("checked", true)
        });
    }

    function clearAll() {
        $formEvents.find('input').prop("checked", false);
    }
});