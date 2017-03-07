

(function(){
   var NovaIdeoWS = window.NovaIdeoWS = window.NovaIdeoWS || {};

   NovaIdeoWS.sock = null;

   NovaIdeoWS.ws_events_handlers = {
      'connection': connection,
      'disconnection': disconnection
   };

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


function connection(params){
   var id = params.id
   $('.user-connection-status[data-oid="'+id+'"]').addClass('connected')
}

function disconnection(params){
   var id = params.id
   $('.user-connection-status[data-oid="'+id+'"]').removeClass('connected')
}

NovaIdeoWS.on('connection', connection)

NovaIdeoWS.on('disconnection', disconnection)

NovaIdeoWS.on('new_comment', function(params){
   var body = params.body;
   var channel_oid = params.channel_oid;
   var channel = $('.channel[data-channel_oid="'+channel_oid+'"]').last()
   var preview = channel.find('>.commentli.comment-preview').first()
   var new_comment = $($(body).find('li.commentli').first())
   new_comment.insertBefore(preview);
   comment_scroll_to(new_comment, true)
   init_emoji($(new_comment.find('.emoji-container:not(.emojified)')));
})


NovaIdeoWS.on('new_answer', function(params){
   var body = params.body;
   var comment_oid = params.channel_oid;
   var comment = $('.channel li[data-comment_id="'+comment_oid+'"]').last()
   var preview = comment.find('>.comments-container>ul.commentul>.commentli.comment-preview').first()
   var new_comment = $($(body).find('li.commentli').first())
   new_comment.insertBefore(preview);
   comment_scroll_to(new_comment, true)
   init_emoji($(new_comment.find('.emoji-container:not(.emojified)')));
})


NovaIdeoWS.on('remove_comment', function(params){
   var channel_oid = params.channel_oid;
   var comment_oid = params.comment_oid;
   var channel = $('.channel[data-channel_oid="'+channel_oid+'"]').last()
   var comment = channel.find('.commentli[data-comment_id="'+comment_oid+'"]')
   comment.addClass('deletion-process')
   comment.animate({height: 0, opacity: 0}, 'slow', function() {
      comment.remove();
   });
})

$(document).on('component_loaded', function() {
   NovaIdeoWS.connect_to_ws_server()
});
