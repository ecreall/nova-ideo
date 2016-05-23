
$(document).ready(function(){

  $(document).on('click','.control-form-button', function(event){
        var form = $($(this).parents('div.ajax-form').first()).find('.controled-form').first();
        if (form.hasClass('hide-bloc')) {
            form.slideDown();
            form.removeClass('hide-bloc')           
        }else{
            form.slideUp();
            form.addClass('hide-bloc')}
    });

    var ajax_forms = $('.ajax-form');
    for(var i=0; i<ajax_forms.length; i++){
        var ajax_form = $(ajax_forms[i]);
       if(ajax_form.find('.has-error, .alert.alert-danger').length>0){
           $(ajax_form.find('.control-form-button').first()).click();
       };
    }
});