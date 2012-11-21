;(function($) {
    var SITE_URL = $(document.body).data('siteUrl');
    var $placeholder = $('#snippet-placeholder');

    window.addEventListener('message', function(e) {
        if (e.origin !== SITE_URL) return;

        $placeholder.html(e.data).find('.snippet').css('display', 'block');
    }, false);
})(jQuery);
