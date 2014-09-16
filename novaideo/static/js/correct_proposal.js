function correct_handler(event){
    var correction = $($(this).parents('#correction').first());
    var vote = Boolean($(this).data('favour'));
    var correction_item = parseInt(correction.data('item'));
    var correction_id = parseInt(correction.data('correction'));
    var target = $($(this).parents('.content-text').first());
    var url = $(this).data('url');
    dict_post = {};
    dict_post['vote'] = vote;
    dict_post['item'] = correction_item;
    dict_post['correction_id'] = correction_id;
    $.get(url, dict_post, function(data) {
      //recuperer le text et le remplacer
      if (data){
        var content = $(data['body']).find('#correction_text');
        if (content){
             $(target).html($(content).html());
             $(target).find('.correction-action').on('click', correct_handler)
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
