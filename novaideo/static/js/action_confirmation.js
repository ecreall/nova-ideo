
$(document).ready(function(){
  $('button .toconfirm').on('click',function(event){
          var form = $($(this).parents('form').first());
          var modal = form.find('.modal.fade');
          $(modal).modal('show');
     });

});

