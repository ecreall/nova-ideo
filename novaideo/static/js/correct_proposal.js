function add_edit_correction_form(oid){
    return '<div data-oid="'+oid+'" aria-hidden="true" role="dialog" class="edit-item-modal-container modal fade">'+
            '<div class="modal-dialog">'+
              '<div class="modal-content">'+
                '<div class="modal-body">'+
                  '<form class="deform edit-item-form">'+
                    '<fieldset class="deform-form-fieldset">'+
                      '<div title="" class="form-group  ">'+
                        '<label class="control-label required" >'+
                         novaideo_translate('Text')+
                        '</label>'+
                        '<textarea id="'+oid+'" class="tinymce form-control"></textarea>'+
                        '<span id="'+oid+'-preload" class="tinymce-preload"></span>'+
                      '</div>'+
                      '<div class="form-group">'+
                          '<button value="edit_item" class="btn btn-primary " name="edit_item" >'+
                            novaideo_translate('Save')+
                          '</button>'+
                          '<button value="Cancel" class="btn btn-default " name="cancel">'+
                            novaideo_translate('Cancel')+
                          '</button>'+
                      '</div></fieldset></form></div></div></div></div>'

}


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
  $.extend(dict_post, get_action_metadata(btn));
  $.post(url, dict_post, function(data) {
    if (data){
      var correction_id = '#correction_'+correction_attr
      var content = $(data['body']).find(correction_id);
      if (content){
           $(target).html($(content).html());
      }
      update_components(data)
    }
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
    $.extend(dict_post, get_action_metadata(correction));
    $.post(url, dict_post, function(data) {
      if (data){
        var correction_id = '#correction_'+correction_attr
        var content = $(data['body']).find(correction_id);
        if (content){
             $(target).html($(content).html());
        }
        update_components(data)
      }
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
    $.extend(dict_post, get_action_metadata(element));
    $.post(url, dict_post, function(data) {
      update_components(data)
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

function init_correction_textarea(oid, lg){
      init_correction_navbar()
      $(document.body).append(add_edit_correction_form(oid))
      window.tinymce.dom.Event.domLoaded = true;
      var jqoid = $('#' + oid);
      var jqoid_preload = $('#' + oid + '-preload');
      jqoid.hide();
      jqoid_preload.click(function(){
        jqoid.show();
        jqoid_preload.remove();
        tinyMCE.init({
          language: lg,
          body_class: 'form-control',
          plugins: ["textcolor"],
         "theme_advanced_resizing_advanced_toolbar_location": "top",
         "toolbar": "undo redo | fontselect fontsizeselect | forecolor backcolor | bold italic",
         "height": 100,
         "theme_advanced_resizing": true,
         "fontsize_formats": "8pt 9pt 10pt 11pt 12pt 13pt 14pt 15pt 26pt 36pt", "skin": "lightgray",
         "strict_loading_mode": true,
         "remove_linebreaks": false,
         "width": 0,
         "theme": "modern",
         "mode": "exact",
          forced_root_block : '',
          invalid_elements : 'p',
          elements: oid
        });
        jqoid_preload.unbind('click');
      });
      jqoid_preload.click();
}

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

