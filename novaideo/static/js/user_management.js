
$(document).ready(function(){
    $('.ajax-form .control-form-button').on('click', function(event){
        var form = $($(this).parents('.ajax-form').find(".controled-form").first());
        var changepassword = $(form.find("input[name='changepassword']").first());
        if(!form.hasClass('hide-bloc')){
            changepassword.prop('checked', true)
        }else{
            changepassword.prop('checked', false)
        }
    });

    if($('.change-password-form .alert').length>0){
       var form = $($('.change-password-form')[0]);
       $($(form.parents('.ajax-form').first()).find('.control-form-button').first()).click();
    };

});
