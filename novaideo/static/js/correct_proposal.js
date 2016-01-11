function correct_handler(event){
    var correction = $($(this).parents('#correction').first());
    var correction_attr = correction.data('content');
    var target = $($(this).parents('.correction-container-'+correction_attr).first());
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

function see_all(){
  $('.correction-container-text del').removeClass('hide-correction');
  $('.correction-container-text ins').removeClass('hide-correction');
  $('.correction-container-text #correction_actions').removeClass('hide-correction');
  $('.correction-container-text #correction').removeClass('hide-correction');
  $('.correction-text-actions li').removeClass('active');
  $($(this).parents('li').first()).addClass('active');
}

function hide_all(){
  $('.correction-container-text del').addClass('hide-correction');
  $('.correction-container-text ins').addClass('hide-correction');
  $('.correction-container-text #correction_actions').addClass('hide-correction');
  $('.correction-container-text #correction').addClass('hide-correction');
  $('.correction-text-actions li').removeClass('active');
  $($(this).parents('li').first()).addClass('active');
}

function correct_all_action(element, vote, correction_attr){
    var url = $(element.parents('ul.correction-text-actions').first()).data('url');
    var target = $($('.correction-container-'+correction_attr).first());
    dict_post = {};
    dict_post['vote'] = vote;
    dict_post['content'] = correction_attr;
    $.get(url, dict_post, function(data) {
      if (data){
        var content = $(data['body']).find('#correction_'+correction_attr);
        if (content){
             $(target).html($(content).html());
             $('.correction-navbar').css('display', 'none');
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

function accept_all(){
    correct_all_action($(this), true, 'text')
}

function refuse_all(){
    correct_all_action($(this), false, 'text')
}

function init_correction_navbar(){
  $('.correction-navbar .correction-text-actions #see-all').on('click', see_all);
  $('.correction-navbar .correction-text-actions #hide-all').on('click', hide_all);
  
  var actions = $('.correction-container-text #correction_actions');
  if (actions.length == 0){
      $('.correction-navbar .correction-text-actions #accept-all').remove();
      $('.correction-navbar .correction-text-actions #refuse-all').remove();
  }else{
    $('.correction-navbar .correction-text-actions #accept-all').on('click', accept_all);
    $('.correction-navbar .correction-text-actions #refuse-all').on('click', refuse_all);
   }
}


$(document).ready(function(){
  $('.correction-action').on('click', correct_handler);
  init_correction_navbar()
});
