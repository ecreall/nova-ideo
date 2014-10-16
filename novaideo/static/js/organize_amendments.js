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
}


function init_select(){
  var element = ($(this).parents('.panel').first()).find('.select-container').last();
  var containers = $(element.parents('.deformSeqContainer').first()).find('.select-container');
  var last_element = $(containers[containers.length-2]);
  var las_title = $($(last_element.parents('.sequence-item').first()).find('.title-select-item').first()).val();
  var list_split = las_title.split('-');
  var id = parseInt(list_split[list_split.length - 1]) + 1;
  var template = $($(element.parents('.deformSeqContainer').first()).find('.deformInsertBefore').first()).attr('item_title');
  $($(element.parents('.sequence-item').first()).find('.title-select-item').first()).val(template+id);
  init_dragdropselect(this); 
  init_remove_button();
};


function scrollto(){
 var source = $('#amendment-diff');
 var element = $(source.find('span[data-item=\''+$(this).data('item')+'\']').first());
 var scrollvalue = source.scrollTop() + element.offset().top - source.offset().top - (source.height()/2);
 source.animate({
    scrollTop: scrollvalue
    }, 1000);

};

 


$(document).ready(function(){
  $('.form-group.explanation-groups label').hide();
   $('.single-amendment-control').click(function(){
        var form = $($(this).parents('form').first());
        if (this.checked) {
            form.find('.form-group.explanation-groups').addClass('hide-bloc');
        }else{
            form.find('.form-group.explanation-groups').removeClass('hide-bloc');
        }
    });
  init_remove_button();
  $('.select-item').on('droped', init_remove_button);
  $('.btn.deformSeqAdd').on('itemadded', init_select); 
  $('.select-item').on('click', scrollto);

  $(document).on('submit','form', function( event ) {
        var button = $(this).find('button');
        if (!$('.single-amendment-control')[0].checked){
          if (button.attr('name') != 'Cancel'){
             var parent = $($(this).parents('.panel-body').first());
             var commentmessagedanger = $(parent.find('#messagedanger'));  
             var items = $('.sequence-item');
             for (i=0; i<items.length; i++){
                 var item = $(items[i]);
                 var selected = $(item.find('select[name="explanations"]'));
                 var values = $($(selected).find("option:selected")).map(function(){ return this.value }).get().join(", ");
                 if (values.length==0){
                     item.addClass('sequence-item-error');
                     $(commentmessagedanger).removeClass('hide-bloc');
                     $( commentmessagedanger.find('.errorMsgLbl')).text( "There was a problem with your submission." ).show();
                     event.preventDefault();
                 }else{ item.removeClass('sequence-item-error')};
             }       
         }
       }
   });


});
