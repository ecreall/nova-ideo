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
  $('.correction-container del').removeClass('hide-correction');
  $('.correction-container ins').removeClass('hide-correction');
  $('.correction-container #correction_actions').removeClass('hide-correction');
  $('.correction-container #correction').removeClass('hide-correction');
  $('.correction-nav-actions li').removeClass('active');
  $($(this).parents('li').first()).addClass('active');
}

function hide_all(){
  $('.correction-container del').addClass('hide-correction');
  $('.correction-container ins').addClass('hide-correction');
  $('.correction-container #correction_actions').addClass('hide-correction');
  $('.correction-container #correction').addClass('hide-correction');
  $('.correction-nav-actions li').removeClass('active');
  $($(this).parents('li').first()).addClass('active');
}


function correct_all_action(element, vote){
    var url = $(element.parents('ul.correction-nav-actions').first()).data('url');
    dict_post = {};
    dict_post['vote'] = vote;
    $.get(url, dict_post, function(data) {
      location.reload();
      });
}

function accept_all(){
    correct_all_action($(this), true);
}

function refuse_all(){
    correct_all_action($(this), false);
}

function init_correction_navbar(){
  $('.correction-navbar .correction-nav-actions #see-all').on('click', see_all);
  $('.correction-navbar .correction-nav-actions #hide-all').on('click', hide_all);
  
  var actions = $('.correction-container #correction_actions');
  if (actions.length == 0){
      $('.correction-navbar .correction-nav-actions #accept-all').remove();
      $('.correction-navbar .correction-nav-actions #refuse-all').remove();
  }else{
    $('.correction-navbar .correction-nav-actions #accept-all').on('click', accept_all);
    $('.correction-navbar .correction-nav-actions #refuse-all').on('click', refuse_all);
   }
}


$(document).ready(function(){
  $('.correction-action').on('click', correct_handler);
  init_correction_navbar()
});
