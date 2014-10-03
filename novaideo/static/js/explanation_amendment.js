function init_explanation_select(){
  $('.explanation-intention').on('change', function(e){
       var intention_bloc = e.val;
       var intention_form = $($($(this).parents('form').first()).find('.'+intention_bloc+'-intention').first());
       var intention_forms = $($($(this).parents('form').first()).find('.form-intention'));
       intention_forms.addClass('hide-bloc')
       if (intention_form.hasClass('hide-bloc')){
           intention_form.removeClass('hide-bloc')
       }
   });
};

function get_explanation_form(url){
              var target = $(this).data('target')+'explanation_modal';
              var url = $(this).data('url');
              $.getJSON(url,{}, function(data) {
                 var action_body = data['body'];
                 if (action_body){
                     $($(target).find('.modal-body')).html(action_body);
                     $(target).modal('show');
                     init_explanation_select();
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

function submit_explanation(url){
       var button = $(this);
       var target = $($(this).parents('.modal.fade').first());
       var selectintention = $(target.find('.explanation-intention').first());
       var intention_bloc = selectintention.select2('val');
       var form = $(selectintention.parents('form').first());
       var intention_form = $(form.find('.'+intention_bloc+'-intention').first());
       var url = $(this).data('url');
       var item = $(this).data('item');

       var comment = $(intention_form.find("textarea[name='comment']").first()).val();
       var ideas = $(intention_form.find("select[name='ideas']").first()).select2('val');
       var replacedideas = $(intention_form.find("select[name='replacedideas']").first()).select2('val');
       var ideasofreplacement = $(intention_form.find("select[name='ideasofreplacement']").first()).select2('val');
       var relatedexplanation = $(form.find("select[name='relatedexplanation']").first()).select2('val');
       var intention = $(form.find("select[name='intention']").first()).select2('val');
       var datas = {'comment': comment,
                   'ideas' : jQuery.makeArray(ideas),
                   'replacedideas': jQuery.makeArray(replacedideas),
                   'ideasofreplacement': jQuery.makeArray(ideasofreplacement),
                   'relatedexplanation': jQuery.makeArray(relatedexplanation),
                   'intention': intention,
                   'item':item
                  };
       $.getJSON(url,datas, function(data) {
             $(target).modal('hide');
             var explanation = $(".btn.explanation-action[data-target=\'#"+button.data('item')+"\']");
             if(intention !='' || (relatedexplanation.length>0 && relatedexplanation[0]!='')){
                explanation.addClass("btn-white");
                explanation.removeClass("btn-black")
             }else{
                explanation.removeClass("btn-white");
                explanation.addClass("btn-black")
              }
       });
       return false;
};

$(document).ready(function(){

  init_explanation_select();

  $(document).on('click', '.explanation-action', get_explanation_form);
  $('.explanation-validation').on('click', submit_explanation);

});

