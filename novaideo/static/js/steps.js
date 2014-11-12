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
            var position = $($(this).parents('li').first()).position();
            var height = $($(this).parents('li').first()).height();
            var top = $($(this).parents('li').first()).position();
            message.css('left', String(position.left)+'px');
            message.css('top', String(position.top+height)+'px');
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

