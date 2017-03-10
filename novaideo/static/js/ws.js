

(function(){
   var NovaIdeoWS = window.NovaIdeoWS = window.NovaIdeoWS || {};

   NovaIdeoWS.sock = null;

   NovaIdeoWS.ws_events_handlers = {};

   NovaIdeoWS.typing_in_process = [];

   NovaIdeoWS.connect_to_ws_server = function(){
      var wsuri;
      var wsuri = "ws://" + window.location.hostname + ":8080/ws";

      if ("WebSocket" in window) {
         NovaIdeoWS.sock = new WebSocket(wsuri);
      } else if ("MozWebSocket" in window) {
         NovaIdeoWS.sock = new MozWebSocket(wsuri);
      } else {
         log("Browser does not support WebSocket!");
      }

      if (NovaIdeoWS.sock) {
         NovaIdeoWS.sock.onopen = function() {
         }

         NovaIdeoWS.sock.onclose = function(e) {
            NovaIdeoWS.sock = null;
         }

         NovaIdeoWS.sock.onmessage = function(e) {
            var data = JSON.parse(e.data)
            // data is a list of events. event = {'event': 'event_id': 'params': {'params_id': value, ...}}
            NovaIdeoWS.call_events_handlers(data)
         }
      }
   };
   
   NovaIdeoWS.trigger_event = function(event) {
      NovaIdeoWS.trigger_events([event])
   };

   NovaIdeoWS.trigger_events = function(events) {
      // events is a list of events. event = {'event': 'event_id': 'params': {'params_id': value, ...}}
      if (NovaIdeoWS.sock) {
         var msg = JSON.stringify(events);
         NovaIdeoWS.sock.send(msg);
      }
   };

   NovaIdeoWS.call_events_handlers = function(events){
       $.each(events, function(index){
          var event_id = this.event
          var op = NovaIdeoWS.ws_events_handlers[event_id]
          op(this.params) 
      })
   };

   NovaIdeoWS.on = function(event_id, callback){
      NovaIdeoWS.ws_events_handlers[event_id] = callback
   };


})();

function increment_channel(channel_oid){
   var channel_action = $('a.channel-action[data-channel_oid="'+channel_oid+'"]').last()
  if(channel_action.length>0){
     var action_container = channel_action.parents('div.channel-action').first()
     action_container.addClass('unread-comments')
     var comment_len_container = action_container.find('.unread-comments-len').first()
     if (comment_len_container.length>0){
        var comment_len = parseInt(comment_len_container.text())+1
        comment_len_container.text(comment_len)
     }else{
        action_container.append('<span class="unread-comments-len pull-right">1</span>')
     }
     alert_user_unread_messages()
     update_unread_messages_alerts()
  }
}

function decrement_channel(channel_oid){
   var channel_action = $('a.channel-action[data-channel_oid="'+channel_oid+'"]').last()
  if(channel_action.length>0){
     var action_container = channel_action.parents('div.channel-action').first()
     var comment_len_container = action_container.find('.unread-comments-len').first()
     if (comment_len_container.length>0){
        var comment_len = parseInt(comment_len_container.text())-1
        if(comment_len==0){
          action_container.removeClass('unread-comments')
          comment_len_container.remove()
        }else{
          comment_len_container.text(comment_len)
        }
     }
  }
}

function connection(params){
   var id = params.id
   $('.user-connection-status[data-oid="'+id+'"]').addClass('connected')
}

function disconnection(params){
   var id = params.id
   $('.user-connection-status[data-oid="'+id+'"]').removeClass('connected')
   //remove typing alerts
   $('.comment-textarea-container .message-alert #'+id).remove()
}

NovaIdeoWS.on('connection', connection)

NovaIdeoWS.on('disconnection', disconnection)

NovaIdeoWS.on('typing_comment', function(params){
   var channel_oid = params.channel_oid;
   var channel = $('.channel[data-channel_oid="'+channel_oid+'"]').last()
   if(channel.length>0){
      var user_name = params.user_name;
      var user_oid = params.user_oid
      var messages_container = channel.parents('.comment-view-block').first()
          .find('.commentform .comment-textarea-container #messageinfo').first()
      var current = messages_container.find('#'+user_oid)
      if(current.length == 0){
       messages_container.append(
         '<span id="'+user_oid+'"><strong>'+user_name+'</strong> '+novaideo_translate("is typing a message")+' <i class="ion-more typing-icon"></i></span>') 
      }
   }
})

function stop_typing_comment(params){
   var channel_oid = params.channel_oid;
   var channel = $('.channel[data-channel_oid="'+channel_oid+'"]').last()
   if(channel.length>0){
      var user_oid = params.user_oid
      var messages_container = channel.parents('.comment-view-block').first()
          .find('.commentform .comment-textarea-container #messageinfo').first()
      var current = messages_container.find('#'+user_oid)
      if(current.length > 0){
       current.remove()
      }
   }
}

NovaIdeoWS.on('stop_typing_comment', stop_typing_comment)

NovaIdeoWS.on('new_comment', function(params){
   var body = params.body;
   var channel_oid = params.channel_oid;
   var channel = $('.channel[data-channel_oid="'+channel_oid+'"]').last()
   if(channel.length>0){
      stop_typing_comment(params)
      var preview = channel.find('>.commentli.comment-preview').first()
      var new_comment = $($(body).find('li.commentli').first())
      new_comment.insertBefore(preview);
      comment_scroll_to(new_comment, true)
      init_emoji($(new_comment.find('.emoji-container:not(.emojified)')));
   }
   if(params.channel_hidden || channel.length == 0){
     increment_channel(params.channel_oid)
   }
})

NovaIdeoWS.on('new_answer', function(params){
   var body = params.body;
   var comment_oid = params.comment_parent_oid;
   var comment = $('.channel li[data-comment_id="'+comment_oid+'"]').last()
   if(comment.length>0){
      stop_typing_comment(params)
      var preview = comment.find('>.comments-container>ul.commentul>.commentli.comment-preview').first()
      var new_comment = $($(body).find('li.commentli').first())
      new_comment.insertBefore(preview);
      comment_scroll_to(new_comment, true)
      init_emoji($(new_comment.find('.emoji-container:not(.emojified)')));
   }
   if(params.channel_hidden || comment.length == 0){
     increment_channel(params.channel_oid)
   }
})

NovaIdeoWS.on('remove_comment', function(params){
   var channel_oid = params.channel_oid;
   var comment_oid = params.comment_oid;
   var channel = $('.channel[data-channel_oid="'+channel_oid+'"]').last()
   if(channel.length>0){
      var comment = channel.find('.commentli[data-comment_id="'+comment_oid+'"]')
      comment.addClass('deletion-process')
      comment.animate({height: 0, opacity: 0}, 'slow', function() {
         comment.remove();
      });
   }
   decrement_channel(channel_oid)
})

NovaIdeoWS.on('edit_comment', function(params){
   var body = params.body;
   var channel_oid = params.channel_oid;
   var comment_oid = params.comment_oid;
   var channel = $('.channel[data-channel_oid="'+channel_oid+'"]').last()
   if(channel.length>0){
      stop_typing_comment(params)
      var comment = channel.find('.commentli[data-comment_id="'+comment_oid+'"]')
      var new_comment = $($(body).find('li.commentli .comment-data').first())
      comment.find('.comment-data').first().replaceWith(new_comment)
      init_emoji($(comment.find('.emoji-container:not(.emojified)')));
      var to_animate = $(comment.find('.comment-data').first())
      if(to_animate.length>0){
       to_animate.animate({
            backgroundColor: "#fff6e5"
       }, 1000, function(){
          to_animate.animate({
            backgroundColor: "white"
       }, 1000 );
       });
     }
   }
})

function user_typing(){
   var input = $(this)
   var channel = input.parents('.comment-view-block').first()
       .find('ul.channel').first()
   var val = input.val()
   var channel_oid = channel.data('channel_oid')
   if(val.length == 0){
      var index = $.inArray(channel_oid, NovaIdeoWS.typing_in_process)
      if(index>=0){
          NovaIdeoWS.typing_in_process = NovaIdeoWS.typing_in_process.splice(index, 1);
      }
      NovaIdeoWS.trigger_event({
         'event': 'stop_typing_comment',
         'params':{
            'channel_oid': channel.data('channel_oid')
         }
      })
   }else if($.inArray(channel_oid, NovaIdeoWS.typing_in_process)<0 && val.length >= 1){
    NovaIdeoWS.typing_in_process.push(channel_oid)
    NovaIdeoWS.trigger_event({
         'event': 'typing_comment',
         'params':{
            'channel_oid': channel.data('channel_oid')
         }
      })
   }
}

function user_stop_typing(){
   var input = $(this)
   var channel = input.parents('.comment-view-block').first()
       .find('ul.channel').first()
   var channel_oid = channel.data('channel_oid')
   var index = $.inArray(channel_oid, NovaIdeoWS.typing_in_process)
   if(index>=0){
      NovaIdeoWS.typing_in_process.splice(index, 1);
      NovaIdeoWS.trigger_event({
         'event': 'stop_typing_comment',
         'params':{
            'channel_oid': channel_oid
         }
       })
   }
}

$(document).on('keypress paste', '.comment-textarea-container textarea', user_typing)

$(document).on('blur', '.comment-textarea-container textarea', user_stop_typing)

$(document).on('component_loaded', function() {
   NovaIdeoWS.connect_to_ws_server()
});

$(document).on('sidebar-opened', function(event){
    var channel = $(event.item).find('ul.channel');
    if(channel.length>0){
      NovaIdeoWS.trigger_event({
         'event': 'channel_opened',
         'params':{
           'channel_oid': channel.data('channel_oid')
         }
      })
   }
})

$(document).on('sidebar-closed', function(event){
   var events = []
   var channels = $(event.items).find('ul.channel');
   if(channels.length>0){
      events = jQuery.makeArray(channels.map(function(){
            return {
            'event': 'stop_typing_comment',
            'params':{
              'channel_oid': $(this).data('channel_oid')
            }}
         })
     )
   }
   events.push({
      'event': 'all_channels_closed',
      'params':{}
   })
   NovaIdeoWS.trigger_events(events)
})

$(document).on('sidebar-items-closed', function(event){
    var channels = $(event.items).find('ul.channel');
    if(channels.length>0){
      NovaIdeoWS.trigger_events(
         jQuery.makeArray(channels.map(function(){return {
            'event': 'channel_hidden',
            'params':{
              'channel_oid': $(this).data('channel_oid')
            }}
         }))
     )
   }
})

$(document).on('comment-removed', function(event){
    NovaIdeoWS.trigger_event({
        'event': 'remove_comment',
        'params':{
          'comment_oid': event.comment_oid,
          'channel_oid': event.channel_oid
        }
     })
})

$(document).on('comment-edited', function(event){
    NovaIdeoWS.trigger_event({
      'event': 'edit_comment',
      'params':{
        'comment_oid': event.comment_oid,
        'channel_oid': event.channel_oid,
        'context_oid': event.context_oid
      }
   })
})

$(document).on('answer-added', function(event){
   NovaIdeoWS.trigger_event({
        'event': 'new_answer',
        'params':{
          'comment_oid': event.comment_oid,
          'comment_parent_oid': event.comment_parent_oid,
          'channel_oid': event.channel_oid,
          'context_oid': event.context_oid
        }
     })
})

$(document).on('comment-added', function(event){
  NovaIdeoWS.trigger_event({
      'event': 'new_comment',
      'params':{
        'comment_oid': event.comment_oid,
        'channel_oid': event.channel_oid,
        'context_oid': event.context_oid
      }
   })
})