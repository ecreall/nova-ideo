

function init_textarea(textarea_id, textarea_limit){
    var desc = $($(textarea_id+'-container').find('#desc').first());
    desc.text("("+textarea_limit+novaideo_translate(" caracteres maximum)"));
    $(textarea_id).textLimit(textarea_limit,function( length, limit, reached ){
        var desc = $($(textarea_id+'-container').find('#desc').first());
        var alert_msg = $($(textarea_id+'-container').find('#alert_message').first()); 
        var nb = limit - length;
        if (length == 0){
            desc.text("("+textarea_limit+novaideo_translate(" caracteres maximum)"));
            alert_msg.addClass('hide-bloc')
          }
        if (reached){
            desc.text('');
            alert_msg.removeClass('hide-bloc')
          }
        if (!reached && length > 0){
            desc.text(nb+novaideo_translate(" remaining characters"));
            alert_msg.addClass('hide-bloc')
          }
    });
};

//source: http://patrickroux.fr/sedetendre/textlimit-le-compteur-jquery-qui-a-du-caractere-1866
(function($){
  $.fn.clearTextLimit=function(){
    return this.each(function(){
      this.onkeydown=this.onkeyup=this.onchange=null;}
  );};
  $.fn.textLimit=function(limit,callback){
      if(typeof callback!=='function')
        var callback=function(){};
      return this.each(function(){
        this.limit=limit;
        this.callback=callback;
        this.onkeydown=this.onkeyup=this.onchange=function(){
          this.value=this.value.substr(0,this.limit);
          this.reached=this.limit-this.value.length;
          this.reached=(this.reached==0)?true:false;
          return this.callback(this.value.length,this.limit,this.reached);}
  });};
})(jQuery);
