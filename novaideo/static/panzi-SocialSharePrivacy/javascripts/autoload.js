jQuery(document).ready(function ($) {
        var socialSharePrivacy = ($.fn.socialSharePrivacy);
	$('*[data-social-share-privacy=true]:not([data-init=true])').
	socialSharePrivacy().attr('data-init','true');
});
