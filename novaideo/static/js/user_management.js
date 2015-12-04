
$(document).ready(function(){
    $('.ajax-form .control-form-button').on('click', function(event){
        var form = $($(this).parents('.ajax-form').find(".controled-form").first());
        var changepassword = $(form.find("input[name='changepassword']").first());
        if(!changepassword.prop('checked')){
            changepassword.prop('checked', true);
        }else{
            changepassword.prop('checked', false);
        }
    });
});
