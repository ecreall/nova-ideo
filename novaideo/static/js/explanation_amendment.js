
intention_schema = ['comment', 'related_ideas']

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
       var intention = $(this).find('select').val();
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

function get_explanation_form(){
              var btn = $(this);
              var modal = $(this).data('target')+'explanation_modal';
              var target = $($('.novaideo-right').children('div').last());
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
                     ($('.content-text').find('.explanation-action.active')).removeClass('active');
                     btn.addClass('active');
                     $('.explanation-validation').on('click', submit_explanation);
                     $('.explanation-close').on('click', close_explanation);
                     target.find('.explanations-bloc').append("<div class=\"intention-separator\">"+novaideo_translate('Or')+"</div>")
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


function close_explanation(){
       var button = $(this);
       ($('.content-text').find('.explanation-action.active')).removeClass('active');
       var parent = $($(this).parents('.explanation-modal').first());
       parent.remove();
}


function submit_explanation(){
       var button = $(this);
       var target = $($(this).parents('.modal-content').first());
       var form = $(target.find('form').first());
       var intention_form = $(form.find('.intention-bloc').first());
       var url = $(this).data('url');
       var item = $(this).data('item');
       var commentmessagedanger = target.find('#messagedanger');
       var comment = $(intention_form.find("textarea[name='comment']").first()).val();
       var related_ideas = $(intention_form.find("select[name='related_ideas']").first()).select2('val');
       var relatedexplanation = "";
       var relatedexplanation_tag = $(form.find("select[name='relatedexplanation']").first());
       if(relatedexplanation_tag.length > 0){
        relatedexplanation = relatedexplanation_tag.select2('val');
       };
       var datas = {'comment': comment,
                   'related_ideas' : related_ideas,
                   'relatedexplanation': relatedexplanation,
                   'item':item
                  };
        if(relatedexplanation == "" && !validate_intention(datas)){
              $( commentmessagedanger).text( novaideo_translate("There was a problem with your submission.") ).show().fadeOut( 4000 );
              return false
        };
       $.getJSON(url,datas, function(data) {
             $(target).modal('hide');
             location.replace(location.href);
       });
       
       return false;
};

function init_explanation(){
      var btn = $(this);
      var target = $(btn.parents('span').first());
      var current_del = $(target.find('dl'))
      if (current_del.length>0){
          var dl = $(current_del.first());
          dl.slideToggle("fast");
          dl.remove();
          btn.removeClass('on');
      }else{
          var dl = $($(btn.data('target')).find('dl').first()).clone(); 
          target.append(dl);
          dl.slideToggle("fast");
          btn.addClass('on');
      }
      
}

$(document).on('click', '.explanation-action', get_explanation_form);

$(document).on('click', '.explanation-comment', init_explanation);

$(document).on('click', '.amendment-toggle', function(){
      var $this = $(this)
      var parent = $($this.parents('.media-body').first())
      parent.toggleClass('small-amendment')
      if($this.hasClass('glyphicon-minus')){
        $this.addClass('glyphicon-plus')
        $this.removeClass('glyphicon-minus')
        $(parent.find("ul.judgment-radio input[type=radio]:not(:checked) ~ .check,"+
          "ul.judgment-radio input[type=radio]:not(:checked) ~ label,"+
          "ul.judgment-radio input[type=radio]:not(:checked)")).hide()
        $(parent.find(".author-block,"+
          ".object-text,"+
          ".majorityjudgment-choices>label")).slideUp()
      }else{
        $this.addClass('glyphicon-minus')
        $this.removeClass('glyphicon-plus')
        $(parent.find("ul.judgment-radio input[type=radio]:not(:checked) ~ .check,"+
          "ul.judgment-radio input[type=radio]:not(:checked) ~ label,"+
          "ul.judgment-radio input[type=radio]:not(:checked)")).show()
        $(parent.find(".author-block,"+
          ".object-text,"+
          ".majorityjudgment-choices>label")).slideDown()
      }
});

$(document).ready(function(){

  init_explanation_select();

});

