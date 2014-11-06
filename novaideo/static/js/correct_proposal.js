function correct_handler(event){
    var correction = $($(this).parents('#correction').first());
    var correction_attr = correction.data('content');
    var target = $($(this).parents('.content-'+correction_attr).first());
    var url = $(this).data('url');
    dict_post = {};
    dict_post['vote'] = Boolean($(this).data('favour'));;
    dict_post['item'] = parseInt(correction.data('item'));
    dict_post['content'] = correction_attr;
    dict_post['correction_id'] = parseInt(correction.data('correction'));
    $.get(url, dict_post, function(data) {
      if (data){
        var content = $(data['body']).find('#correction_'+correction_attr);
        if (content){
             $(target).html($(content).html());
             var corrections = $(target).find('.correction-action');
             if (corrections.length>0){
                 corrections.on('click', correct_handler)
             }else{
                 location.reload();
             }
        }else{
           location.reload();
           return false
         };
      }else{
           location.reload();
           return false
         };
      });
    
   }

$(document).ready(function(){
  
  $('.correction-action').on('click', correct_handler);

});
