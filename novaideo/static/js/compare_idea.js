$(document).ready(function(){

    $(document).on('submit','.compareform', function( event ) {
        var button = $(this).find('button')

        var parent = $($(this).parents('.panel-body').first());
        var target = parent.find('.compare-result');
        //POST dict
        var dict_post = {};
        var inputs = $($(event.target).children().filter('fieldset')[0]).find('input[type|="radio"]');
        var version = '';
        for (i=0; i<inputs.length; i++ ){
           if (inputs[i].checked){version = $(inputs[i]).val()};
        };
        dict_post['version'] = version;
        var url = $(event.target).data('url');
        if (version !=''){
          loading_progress()
          $(button).addClass('disabled');
          $.get(url, dict_post, function(data) {
                 var content = $(data).find('.compare-result');
                 if (content){
                     $(target).html($(content).html());
                  }else{
                     location.reload();
                     return false
                  };
                  $(button).removeClass('disabled');
              });
              finish_progress();
        }else{
           var errormessage = '';
           if (intention == ''){
               errormessage =  "intention";
           };
           if (comment == ''){
              if (errormessage != ''){errormessage=errormessage+' and comment'}else{errormessage = 'comment'}
           };

       };
       event.preventDefault();
   });

});
