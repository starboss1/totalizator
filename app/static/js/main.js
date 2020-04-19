$(function () {
    const navCollapse = 767;
    const $nav = $('nav');
    const $mainDiv = $("#main-div");

    //dropdown on hover on desktop
    $('.dropdown').hover(
        function () {
            if ($(window).width() > navCollapse) {
                $(this).addClass('show');
                $(this).find('.dropdown-menu').addClass('show')
            }
        },
        function () {
            if ($(window).width() > navCollapse) {
                $(this).removeClass('show');
                $(this).find('.dropdown-menu').removeClass('show')
            }
        },
    );

    addNavbarPaddingTop();

    function addNavbarPaddingTop() {
        $mainDiv.css('padding-top', $nav.outerHeight());
    }
});