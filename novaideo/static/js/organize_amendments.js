function init_remove_button(){
  var removeactions = $('.remove-item');
  for (i=0; i<removeactions.length; i++){
    var seqremove = removeactions[i];
    var element = ($(seqremove).parents('.sequence-item').first()).find('.select-container').last();
    if ($(element).find('.select-item').length >0){
       $(seqremove).removeClass('remove-item');
       $(seqremove).addClass('disabled-remove-item');
       $(seqremove).attr('onclick', 'javascript:return false')
       
     }
 };

  var disabledremoveactions = $('.disabled-remove-item');
  for (i=0; i<disabledremoveactions.length; i++){
    var seqremove = disabledremoveactions[i];
    var element = ($(seqremove).parents('.sequence-item').first()).find('.select-container').last();
    if ($(element).find('.select-item').length == 0){
       $(seqremove).removeClass('disabled-remove-item');
       $(seqremove).addClass('remove-item');
       $(seqremove).attr('onclick', "javascript:deform.removeSequenceItem(this);")
     }
 };
};


function init_justification(){
  var justification = $($(this).parents('.sequence-item').first().find('.justification-select-item').first());
  if(justification.val() == ''){
    var source = $('#amendment-diff');
    var element = $(source.find('span[data-item=\''+$(this).data('item')+'\']').first());
    var comment = $($(element.find('#explanation_action > button').first()).data('target')+' dd#comment');
    if(comment.length>0){
      justification.val(comment.text())
    }
    
 }
};


function init_select(){
  var element = ($(this).parents('.drag-drop-panel').first()).find('.select-container').last();
  var containers = $(element.parents('.deform-seq-container').first()).find('.select-container');
  var last_element = $(containers[containers.length-2]);
  var las_title = $($(last_element.parents('.sequence-item').first()).find('.title-select-item').first()).val();
  var list_split = las_title.split('-');
  var id = parseInt(list_split[list_split.length - 1]) + 1;
  var template = $($(element.parents('.deform-seq-container').first()).find('.deform-insert-before').first()).attr('item_title');
  $($(element.parents('.sequence-item').first()).find('.title-select-item').first()).val(template+id);
  init_dragdropselect(this); 
  init_remove_button();
  var justification = $(($(this).parents('.drag-drop-panel').first()).find('.justification-select-item').last());
  justification.elastic();
  try{
      init_textarea("#"+justification.attr('id'), parseInt(justification.data('limit')));
  }catch(err){

  }
};


function scrollto(){
 var source = $('#amendment-diff');
 var element = $(source.find('span[data-item=\''+$(this).data('item')+'\']').first());
 var scrollvalue = source.scrollTop() + element.offset().top - source.offset().top - (source.height()/2);
 var explanation = $($(element.find('#explanation_action').first()).find('dl.explanation-detail').first());
 source.animate({
    scrollTop: scrollvalue
    }, 500);
 if (explanation.length==0){
    $(element.find('button').first()).click() 
 }
 
};

function init_explanation_item(){
      var btn = $(this);
      var target = $(btn.parents('span').first());
      var current_del = $(target.find('dl'))
      if (current_del.length>0){
          var dl = $(current_del.first());
          dl.slideToggle("fast");
          dl.remove();
          btn.removeClass('explanation-comment-on');
      }else{
          var dl = $($(btn.data('target')).find('dl').first()).clone(); 
          target.append(dl);
          dl.slideToggle("fast");
          btn.addClass('explanation-comment-on');
      }
      
}

$(document).on('submit','form', function( event ) {
    var button = $(event['originalEvent']['explicitOriginalTarget'])
    var btn_name = button.attr('name');
    if (btn_name != 'Cancel'){
      var parent = $($(this).parents('.panel-body').first());
      var commentmessagedanger = $(parent.find('#messagedanger'));
      if (!$('.single-amendment-control')[0].checked){
        if (button.attr('name') != 'Cancel'){  
           var items = $('.sequence-item:not(.header)');
           for (i=0; i<items.length; i++){
               var item = $(items[i]);
               var selected = $(item.find('select[name="explanations"]'));
               var values = $($(selected).find("option:selected")).map(function(){ return this.value }).get().join(", ");
               var justification = $(item.find('textarea.justification-select-item').first());
               var justification_val = justification.val();
               if (justification_val == "" ){
                   item.addClass('sequence-item-error');
                   item.addClass('has-error');
                   $(commentmessagedanger).removeClass('hide-bloc');
                   $( commentmessagedanger.find('.errorMsgLbl')).text(novaideo_translate("There was a problem with your submission.")).show();
                   event.preventDefault();
               }else{ 
                    item.removeClass('sequence-item-error');
                    item.removeClass('has-error');
                     };
           }       
       }
     }else{
       var justification = $(parent.find('.form-group.justification-amendment').first());
       var justification_val = $(justification.find('textarea').first()).val();
       if (justification_val == ""){
          justification.addClass('has-error');
          $(commentmessagedanger).removeClass('hide-bloc');
          $( commentmessagedanger.find('.errorMsgLbl')).text(novaideo_translate("There was a problem with your submission.")).show();
          event.preventDefault();
       }else{
         justification.removeClass('has-error');
       }
     }
   }
 });

$(document).on('click', '.explanation-item', init_explanation_item);


$(document).ready(function(){
  $('.form-group.explanation-groups label').hide();

  $('.single-amendment-control').click(function(){
        var form = $($(this).parents('form').first());
        if (this.checked) {
            form.find('.form-group.explanation-groups').addClass('hide-bloc');
            form.find('.form-group.justification-amendment label').addClass('required');
            form.find('.form-group.justification-amendment').removeClass('hide-bloc');
        }else{
            form.find('.form-group.explanation-groups').removeClass('hide-bloc');
            form.find('.form-group.justification-amendment').addClass('hide-bloc');
        }
    });

  init_remove_button();

  $('.select-item').on('droped', init_remove_button);

  $('.select-item').on('droped', init_justification);

  $('.add-amendment-item.deform-seq-add').on('itemadded', init_select); 

  $('.select-item').on('click', scrollto);

  $('.justification-select-item').elastic();

});
