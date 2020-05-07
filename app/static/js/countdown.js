$(function () {
    $("[data-countdown]").each(function () {
        const $this = $(this);
        const countDownDate = new Date($this.data("countdown")).getTime();

        let x = setInterval(function updateCountdown() {
            // Get todays date and time
            let now = new Date().getTime();

            // Find the diff between now and the count down date
            let diff = countDownDate - now;

            // Time calculations for days, hours, minutes and seconds
            let days = Math.floor(diff / (1000 * 60 * 60 * 24));
            let hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((diff % (1000 * 60)) / 1000);

            $this.find(".js-days").text(days);
            $this.find(".js-hours").text(hours);
            $this.find(".js-minutes").text(minutes);
            $this.find(".js-seconds").text(seconds);

            // If the count down is finished, write some text
            if (diff < 0) {
                clearInterval(x);
                $this.hide()
            }
            return updateCountdown;
        }(), 1000);
    });
});