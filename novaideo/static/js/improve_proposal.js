
$(document).ready(function(){
  $('button.toconfirm').on('click',function(event){
         var form = $($(this).parents('form').first());
         var confirmation = form.find('.modal.fade');
         $(confirmation).modal('show');

     });

});

