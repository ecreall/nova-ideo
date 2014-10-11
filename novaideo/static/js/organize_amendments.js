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
  init_remove_button();
  $('.select-item').on('droped', init_remove_button);
  $('.btn.deformSeqAdd').on('itemadded', init_select); 
  $('.select-item').on('click', scrollto);
});
