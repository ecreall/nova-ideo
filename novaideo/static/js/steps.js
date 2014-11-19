
chronos = { }

function get_chrono_expired_msg(){
    return "<span style=\"color:#d9534f;\" >"+novaideo_translate('Period expired')+"</span>"
}

function set_step_time(target){
    var secon = $($(target).find('#secon').first())
    var minu = $($(target).find('#minu').first())
    var hour = $($(target).find('#hour').first())
    var day = $($(target).find('#day').first())
    var chrono_item = chronos[target]
    if (secon.length > 0){chrono_item['secon'] = parseInt(secon.text())};
    if (minu.length > 0){chrono_item['minu'] = parseInt(minu.text())};
    if (hour.length > 0){chrono_item['hour'] = parseInt(hour.text())};
    if (day.length > 0){chrono_item['day'] = parseInt(day.text())}
}

function add_chrono(target){
  chronos[target] = { 
              'secon': 1,
              'minu': 0,
              'hour': 0,
              'day': 0};
  set_step_time(target)
}

function chrono_is_expired(chrono_item){
   return chrono_item['secon']==0 && chrono_item['minu']==0 && chrono_item['hour']==0 && chrono_item['day']==0

}

function chrono(target){
    var chrono_item = chronos[target]
    chrono_item['secon']--;
    if (chrono_item['secon']<0 && chrono_item['minu']>0){chrono_item['secon']=59;chrono_item['minu']--};
    if (chrono_item['minu']<0 && chrono_item['hour']>0){chrono_item['minu']=59;chrono_item['hour']--};
    if (chrono_item['hour']<0 && chrono_item['day']>0){chrono_item['hour']=23;chrono_item['day']--};
    var secon = $($(target).find('#secon').first())
    var minu = $($(target).find('#minu').first())
    var hour = $($(target).find('#hour').first())
    var day = $($(target).find('#day').first())
    if (secon.length > 0){secon.text(chrono_item['secon'])};
    if (minu.length > 0){minu.text(chrono_item['minu'])};
    if (hour.length > 0){hour.text(chrono_item['hour'])};
    if (day.length > 0){day.text(chrono_item['day'])};
    if (! chrono_is_expired(chrono_item)){
       compte=setTimeout(function(){chrono(target)},1000)
    }else{
       $(target).replaceWith(get_chrono_expired_msg())
    }
}

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

