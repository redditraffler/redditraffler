$(function() {
    // Show/hide functionality for navbar burger
    var $navbarBurgers = $('.navbar-burger');
    if ($navbarBurgers.length > 0) {
        $navbarBurgers.each(function() {
            $(this).click(function() {
                var $target = $('#'+$(this).attr('data-target'));
                $(this).toggleClass('is-active');
                $target.toggleClass('is-active');
            });
        });
    }

    // Logout button click handler
    if ($("#logout").length > 0) {
        $("#logout").click(function() {
            $("#logout-form").submit();
        });
    }
});
