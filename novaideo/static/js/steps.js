var inprogress = false;

$(document).ready(function(){
    $('.step-content').on('click', function(){
        var message = $($($(this).parents('.steps').first()).find('#'+$(this).data('step')).first());
        if (message.hasClass('in')){
            message.removeClass('in');
            $(this).removeClass('message-in');
            $(message).css('z-index', '-1010');
            inprogress = false
        }else{
            $(message).css('z-index', '1010');
            message.addClass('in');
            var left = $($(this).parents('li').first()).position().left-80;
            message.css('left', String(left)+'px');
            $(this).addClass('message-in');
            inprogress = true

       }
    });

    $(document).on('click', function(event){
       if(!inprogress){
           $('.step-content.message-in').click();
       }else{
           inprogress = false
       }
    });
});

