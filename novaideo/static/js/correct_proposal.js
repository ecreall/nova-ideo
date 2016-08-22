function show_edit_item_form(event){
    var parent = $($(this).parents('#correction').first())
    var correction = $(parent.find('ins').first());
    var modal = $('.edit-item-modal-container')
    var oid = modal.data('oid')
    tinyMCE.get(oid).setContent(correction.html());
    modal.modal('show')
    parent.addClass('active-correction')

}

function edit_item(form){
  var modal = $(form.parents('.edit-item-modal-container').first())
  var oid = modal.data('oid')
  var text = tinyMCE.get(oid).getContent();
  var correction = $($('#correction.active-correction').first())
  var correction_attr = correction.data('content');
  var btn = $(correction.find('.edit-item-action').first())
  var target = $(btn.parents('.correction-container-'+correction_attr).first());
  var url = btn.data('url');
  dict_post = {};
  dict_post['vote'] = Boolean(btn.data('favour'));
  dict_post['item'] = parseInt(correction.data('item'));
  dict_post['content'] = correction_attr;
  dict_post['correction_id'] = parseInt(correction.data('correction'));
  dict_post['edited'] = true
  dict_post['new_text'] = text
  modal.modal('hide')
  $.get(url, dict_post, function(data) {
    if (data){
      var content = $(data['body']).find('#correction_'+correction_attr);
      if (content){
           $(target).html($(content).html());
           var corrections = $(target).find('.correction-action');
           if (corrections.length==0){
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


function correct_handler(event){
    var correction = $($(this).parents('#correction').first());
    var correction_attr = correction.data('content');
    var target = $($(this).parents('.correction-container-'+correction_attr).first());
    var url = $(this).data('url');
    dict_post = {};
    dict_post['vote'] = Boolean($(this).data('favour'));
    dict_post['item'] = parseInt(correction.data('item'));
    dict_post['content'] = correction_attr;
    dict_post['correction_id'] = parseInt(correction.data('correction'));
    $.get(url, dict_post, function(data) {
      if (data){
        var content = $(data['body']).find('#correction_'+correction_attr);
        if (content){
             $(target).html($(content).html());
             var corrections = $(target).find('.correction-action');
             if (corrections.length==0){
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
  $(document).on('click', '.correction-action:not(.edit-item-action)', correct_handler);
  $(document).on('click', '.edit-item-action', show_edit_item_form);
  $(document).on('click', '.edit-item-modal-container button', function(){
       $(this).addClass('active')
  });
  $(document).on('submit','.edit-item-form', function( event ) {
    var form = $(this)
    var button = $(form.find('button.active').first())
    if (button.attr('name') == 'cancel'){
      $(form.parents('.edit-item-modal-container').first()).modal('hide')
      $('#correction.active-correction').removeClass('active-correction')
    }else{
      edit_item(form)
    }
    event.preventDefault();
  })
  init_correction_navbar()
});
