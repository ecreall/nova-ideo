
intention_schema = ['comment', 'edited_ideas', 'added_ideas', 'removed_ideas']


function validate_intention(datas){
    return (datas['comment'].length>0)

    for (i=0; i<intention_schema.length; i++){
        if (datas[intention_schema[i]].length==0){
            return false
       }
    };
    return true
};


function init_explanation_select(){

  $('.related-explanation').on('change', function(e){
       var intention = e.val;
       var form = $($(this).parents('form').first());
       if (intention != ''){
           form.find('.intention-bloc').addClass('hide-bloc');
           form.find('.intention-separator').addClass('hide-bloc');
       }else{
           form.find('.intention-bloc').removeClass('hide-bloc')    
           form.find('.intention-separator').removeClass('hide-bloc');    

       }
   });


};

function get_explanation_form(url){
              var btn = $(this);
              var modal = $(this).data('target')+'explanation_modal';
              var target = $($('.novaideo-right').find('div').first());
              var url = $(this).data('url');
              
              $.getJSON(url,{}, function(data) {
                 var action_body = data['body'];
                 if (action_body){
                     var modal_content = $($(modal).find('.modal-dialog')); 
                     target.html(modal_content.html());
                     var modal_body = $(target.find('.modal-body')); 
                     modal_body.html(action_body);
                     $(target.find('.modal-content')).addClass('explanation-modal');
                     target.show();
                     init_explanation_select();
                     ($('.content-text').find('.explanation-action.btn-blue')).removeClass('btn-blue');
                     btn.addClass('btn-blue');
                     $('.explanation-validation').on('click', submit_explanation);
                     $('.explanation-close').on('click', close_explanation);
                     target.find('.explanations-bloc').append("<div class=\"intention-separator\">Or</div>")
                     try {
                          deform.processCallbacks();
                      }
                     catch(err) {};
                  }else{
                     location.reload();
                     return false
                  }
              });
              return false;
};

function get_data(selecteds){
    var selecteds = jQuery.makeArray(selecteds);
    var result= [];
    for(i=0;i<selecteds.length; i++){
       result[i] = selecteds[i].id
    };
    return result
};

function close_explanation(url){
       var button = $(this);
       ($('.content-text').find('.explanation-action.btn-blue')).removeClass('btn-blue');
       var parent = $($(this).parents('.explanation-modal').first());
       parent.remove();
}


function submit_explanation(url){
       var button = $(this);
       var target = $($(this).parents('.modal-content').first());
       var form = $(target.find('form').first());
       var intention_form = $(form.find('.intention-bloc').first());
       var url = $(this).data('url');
       var item = $(this).data('item');
       var commentmessageinfo = target.find('#messageinfo');
       var commentmessagesuccess = target.find('#messagesuccess');
       var commentmessagedanger = target.find('#messagedanger');
       var comment = $(intention_form.find("textarea[name='comment']").first()).val();
       var added_ideas = $(intention_form.find("select[name='added_ideas']").first()).select2('data');
       var removed_ideas = $(intention_form.find("select[name='removed_ideas']").first()).select2('data');
       var edited_ideas = $(intention_form.find("select[name='edited_ideas']").first()).select2('data');
       var relatedexplanation = $(form.find("select[name='relatedexplanation']").first()).select2('val');
       if (!(typeof relatedexplanation == "string")){relatedexplanation=""};
       var datas = {'comment': comment,
                   'added_ideas' : get_data(added_ideas),
                   'removed_ideas': get_data(removed_ideas),
                   'edited_ideas': get_data(edited_ideas),
                   'relatedexplanation': relatedexplanation,
                   'item':item
                  };
        if(relatedexplanation == "" && !validate_intention(datas)){
              $( commentmessagedanger).text( "There was a problem with your submission." ).show().fadeOut( 4000 );
              return false
        };
       $.getJSON(url,datas, function(data) {
             $(target).modal('hide');
             location.reload();
             /*var explanation = $(".btn.explanation-action[data-target=\'#"+button.data('item')+"\']");
             if(intention !='' || (relatedexplanation.length>0 && relatedexplanation[0]!='')){
                explanation.addClass("btn-white");
                explanation.removeClass("btn-black")
             }else{
                explanation.removeClass("btn-white");
                explanation.addClass("btn-black")
              }*/
       });
       return false;
};

$(document).ready(function(){

  init_explanation_select();

  $(document).on('click', '.explanation-action', get_explanation_form);
 // $('.explanation-validation').on('click', submit_explanation);

});

//TODO on change pour les selects : supprimer ce qu'il faut.
//TODO ajout nouvel idee: il faut l'ajouter aux selects

