

function init_btn_control(btn){
   $(btn).click(function(){
        var form = $($(this).parents('.ajax-form').first());
        var new_idea_form = $(form.find('.new-idea-form').first());
        if (new_idea_form.hasClass('hide-bloc')) {
            new_idea_form.removeClass('hide-bloc')            
        }else{
            new_idea_form.addClass('hide-bloc') 
        }
    });
};


$(document).on('click','.new-idea-form button.ajax-button.validate-btn', function( event ) {
    var button = $(this);
    var form = $(button.parents('.new-idea-form').first());
    var danger_messages_container = $($(form.parents('.ajax-form').first()).find('#messagedanger'));
    var success_messages_container = $($(form.parents('.ajax-form').first()).find('#messagesuccess'));
    var dict_post = {};
    var title = form.find('input[name="title"]').val();
    if (title =='')
    {
       alert_component({
              alert_msg: novaideo_translate("The title is required!"),
              alert_type: 'error'
       })
       return
    }
    var text = form.find('textarea[name="text"]').val();
    if (text =='')
    {
       alert_component({
              alert_msg: novaideo_translate("The abstract is required!"),
              alert_type: 'error'
       })
       return
    }

    var keywords = $(form.find('select[name="keywords"]')).val();
    if (keywords.length == 0)
    {
       alert_component({
              alert_msg: novaideo_translate("Keywords are required!"),
              alert_type: 'error'
          })
       return
    }

    dict_post = {'title': title,
                 'text': text,
                 'keywords': keywords,
                 'op': 'creat_idea'};

     var url = $(button).data('url');
     button.addClass('disabled');
     loading_progress()
     $.get(url, dict_post, function(data) {
         if(data){
           button.removeClass('disabled'); 
           form.find('input[name="title"]').val('');
           form.find('textarea[name="text"]').val('');
           alert_component({
                  alert_msg: "The idea \""+dict_post['title']+"\" is added",
                  alert_type: 'success'
              })
           form.addClass('hide-bloc');
         }else{
            alert_component({
                  alert_msg: novaideo_translate("The idea is not added!"),
                  alert_type: 'error'
              })
         }
         finish_progress()
    });
});
keywords