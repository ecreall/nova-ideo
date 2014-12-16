

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


$(document).ready(function(){
    $(document).on('click','.new-idea-form button.ajax-button.validate-btn', function( event ) {
        var button = $(this);
        var form = $(button.parents('.new-idea-form').first());
        var danger_messages_container = $($(form.parents('.ajax-form').first()).find('#messagedanger'));
        var success_messages_container = $($(form.parents('.ajax-form').first()).find('#messagesuccess'));
        var dict_post = {};
        var title = form.find('input[name="title"]').val();
            if (title=='')
            {
               danger_messages_container.text( novaideo_translate("The title is required!") ).show().fadeOut( 6000 );
               return
            }
            var text = form.find('textarea[name="text"]').val();
            if (text=='')
            {
               danger_messages_container.text( novaideo_translate("The abstract is required!") ).show().fadeOut( 6000 );
               return
            }

            var keywords = $(form.find('select[name="keywords"]')).select2('val');
            if (keywords.length == 0)
            {
               danger_messages_container.text( novaideo_translate("Keywords are required!") ).show().fadeOut( 6000 );
               return
            }

            dict_post = {'title': title,
                         'text': text,
                         'keywords': keywords,
                         'op': 'creat_idea'};

         var url = $(button).data('url');
         button.addClass('disabled');
         $.get(url, dict_post, function(data) {
             if(data){
               button.removeClass('disabled'); 
               form.find('input[name="title"]').val('');
               form.find('textarea[name="text"]').val('');
               $(form.find('select[name="keywords"]')).select2('val', []);
               success_messages_container.text( "The idea \""+dict_post['title']+"\" is added" ).show().fadeOut( 6000 );
               form.addClass('hide-bloc');
             }else{
                danger_messages_container.text( novaideo_translate("The idea is not added!") ).show().fadeOut( 6000 );
             }
        });
   });
})
