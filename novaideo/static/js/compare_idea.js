$(document).on('submit','.compareform', function( event ) {
    var $this = $(this)
    var button = $this.find('button')
    var parent = $($this.parents('.compare-block').first());
    var target = $(parent.find('.compare-result'));
    //POST dict
    var dict_post = {};
    var inputs = $($(event.target).children().filter('fieldset')[0]).find('input[type|="radio"]');
    var version = '';
    for (i=0; i<inputs.length; i++ ){
       if (inputs[i].checked){version = $(inputs[i]).val()};
    };
    dict_post['version'] = version;
    var url = $(event.target).data('url');
    if (version !=''){
      loading_progress()
      $(button).addClass('disabled');
      $.get(url, dict_post, function(data) {
             var content = $(data).find('.compare-result');
             if (content){
                 target.html($(content).html());
                 init_content_text_scroll(target.find(".content-text-scroll"))
                 rebuild_scrolls(target.find(".malihu-scroll"))
              }else{
                 location.reload();
                 return false
              };
              $(button).removeClass('disabled');
              finish_progress();
          });
    }else{
      alert_component({
          alert_msg: novaideo_translate("Please select a version!"),
          alert_type: 'error'
        })
   };
   event.preventDefault();
});
