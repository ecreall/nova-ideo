
function _is_unique(){
    var data = $('#publication-data');
    if(data.length>0){
      var is_unique = data.data('is_unique')
      if(is_unique){
        return is_unique
      }else{
        var wiki = $("input[type='radio'][value='wiki']");
        if(wiki.length>0 &&  wiki.prop('checked')){
                return true
        }else{
          return is_unique
        }
      }
    }
    return false
}

$(document).on('click', ".publish-proposal-form input[type='radio'][value='True']", function(event){
  // if(_is_unique()){
    var $this = $(this);
    if($this.prop('checked')){
          $('.work-duration').addClass('hide-bloc')
          $('.work-mode').addClass('hide-bloc')
    }
  // }
})

$(document).on('click', ".publish-proposal-form input[type='radio'][value='False']", function(event){
  // if(_is_unique()){
    var $this = $(this);
    if($this.prop('checked')){
          $('.work-duration').removeClass('hide-bloc')
          $('.work-mode').removeClass('hide-bloc')
    }
  // }
})

$(document).on('click', ".publish-proposal-form input[type='radio'][value='wiki']", function(event){
  if($("input[type='radio'][value='True']").prop('checked')){
          $('.work-duration').addClass('hide-bloc')
          $('.work-mode').addClass('hide-bloc')
  }
})

$(document).ready(function(){
  $('button.ajax-button').on('click',function(event){
         var form = $($(this).parents('form').first());
         var confirmation = form.find('.modal.fade');
         $(confirmation).modal('show');

     });

});

