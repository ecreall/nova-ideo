
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
    var total = chrono_item['minu']+chrono_item['hour']+chrono_item['day'];
    if (chrono_item['secon']<0 && total>0){chrono_item['secon']=59;chrono_item['minu']--};
    total = chrono_item['hour']+chrono_item['day'];
    if (chrono_item['minu']<0 && total>0){chrono_item['minu']=59;chrono_item['hour']--};
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


function open_step_message(step, message){
    message.css('z-index', '1010');
    message.addClass('in');
    var step_li = $(step.parents('li').first());
    var height = step_li.height();
    var element_by_media = step_li;
    //responsive design
    try{
      if (window.matchMedia('(max-width: 991px)').matches) {
         element_by_media = $('body');
      };
    }catch(err){
    }
    var offset = element_by_media.offset();
    var element_by_media_width = element_by_media.width();
    var message_wdth = message.width();
    var width = element_by_media_width/2 - message_wdth/2;
    message.css('left', String(offset.left + (width))+'px');
    message.css('top', String(step_li.offset().top+height-10)+'px');
    message.show();
    step_li.addClass('message-in');
}

function close_step_messages(){
  var messages = $('.in.step-message');
  messages.removeClass('in');
  messages.hide();
  $(messages).css('z-index', '-1010');
  $('li.message-in').removeClass('message-in')
}

$(document).on('click' ,function(event){
   var parents = $($(event.target).parents('.message-in, .in.step-message'))
   if(parents.length == 0){
     close_step_messages()
   }
});

function init_step_contents(){
  $('li.active .step-content').hover(function(){
        close_step_messages()
        var $this = $(this)
        var message = $($('#steps-messages').find('#'+$this.data('step')).first());
        open_step_message($this, message)
    })
}

$(document).ready(function(){
    init_step_contents()
});

