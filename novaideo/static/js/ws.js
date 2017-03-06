

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
      NovaIdeoWS.send_events([event])
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

$(document).on('component_loaded', function() {
   NovaIdeoWS.connect_to_ws_server()
});
