
$(document).ready(function(){
  $('button.ajax-button').on('click',function(event){
         var form = $($(this).parents('form').first());
         var confirmation = form.find('.modal.fade');
         $(confirmation).modal('show');

     });

});

