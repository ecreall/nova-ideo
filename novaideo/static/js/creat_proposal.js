
$(document).ready(function(){
  
  $($($(".form-proposal-confirmation").parents('form').first()).find('button').not('[value*="Cancel"]').first()).addClass('disabled');

  $(".form-idea-select select").on("change", function(e) { 
     var form = $($(this).parents('form').first());
     var button = form.find('button').not('[value*="Cancel"]').first();
     if (e.val.length == 0){
        $(".form-proposal-confirmation").hide();
        $(button).addClass('disabled');
        
     }else{
        $(".form-proposal-confirmation").show();
        $(button).removeClass('disabled');
     }
     
  });

});
