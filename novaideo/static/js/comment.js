$(document).ready(function(){

    $(document).on('submit','.commentform', function( event ) {
        var button = $(this).find('button')

        var intention = $(this).find('.select2-chosen').text();
        var textarea = $(this).find('textarea');
        var comment = textarea.val();

        var parent = $($(this).parents('.panel-body').first());
        var target = parent.find('.scroll-able.comments-scroll');
        var commentmessageinfo = parent.find('#commentmessageinfo');
        var commentmessageinfo = parent.find('#commentmessageinfo');
        var commentmessagesuccess = parent.find('#commentmessagesuccess');
        var commentmessagedanger = parent.find('#commentmessagedanger');
        var progress = parent.find('#progress');
        //POST dict
        var dict_post = {};
        var inputs = $($(event.target).children().filter('fieldset')[0]).children().filter('input');
        var i = 0;
        while(i<inputs.length){
           dict_post[$(inputs[i]).attr('name')] = $(inputs[i]).val();
           i++;
        };
        dict_post['comment'] = comment;
        dict_post['intention'] = intention;
        dict_post[button.val()] = '';
        var url = $(event.target).data('url');
        if (comment !='' && intention!=''){
          progress.show();// TODO
          $(button).addClass('disabled');
          $( commentmessageinfo).text( "Comment sent" ).show().fadeOut( 1000 );
          $.post(url, dict_post, function(data) {
                 var content = $(data).find('.scroll-able.comments-scroll');//TODO chercher le bon scrollable
                 if (content){
                     $(target).html($(content).html());
                     $( commentmessagesuccess).text( "Your comment is integrated" ).show().fadeOut( 3000 );
                     textarea.val('')
                  }else{
                     location.reload();
                     return false
                  };
                  $(button).removeClass('disabled');
              });
              progress.hide();
        }else{
           var errormessage = '';
           if (intention == ''){
               errormessage =  "intention";
           };
           if (comment == ''){
              if (errormessage != ''){errormessage=errormessage+' and comment'}else{errormessage = 'comment'}
           };
           $( commentmessagedanger).text( "Your "+errormessage+" cannot be empty!" ).show().fadeOut( 4000 );

       };
       event.preventDefault();
   });

    $(document).on('submit','.respondform', function( event ) {
        var formid = $(this).attr('id');
        var button = $(this).find('button')

        var intention = $(this).find('.select2-chosen').text();
        var textarea = $(this).find('textarea');
        var comment = textarea.val();

        var parent = $($(this).parents('.panel-body').get(1));
        var modal = $(parent).find('.modal.fade:has(form[id|=\''+formid+'\'])');
        var parentform = parent.find('.commentform');
        var urlparent = $(parentform).data('url');

        var target = parent.find('.scroll-able.comments-scroll');
        var commentmessageinfo = parent.find('#commentmessageinfo');
        var commentmessageinfo = parent.find('#commentmessageinfo');
        var commentmessagesuccess = parent.find('#commentmessagesuccess');
        var commentmessagedanger = parent.find('#commentmessagedanger');
        var progress = parent.find('#progress');
        //POST dict
        var dict_post = {};
        var inputs = $($(event.target).children().filter('fieldset')[0]).children().filter('input');
        var i = 0;
        while(i<inputs.length){
           dict_post[$(inputs[i]).attr('name')] = $(inputs[i]).val();
           i++;
        };
        dict_post['comment'] = comment;
        dict_post['intention'] = intention;
        dict_post[button.val()] = '';

        var url = $(event.target).data('url');
        if (comment !='' && intention!=''){
          progress.show();// TODO
          $(modal).modal('hide');
          $( commentmessageinfo).text( "Comment sent" ).show().fadeOut( 1000 );
          $.post(url, dict_post, function(data) {
                 $( commentmessagesuccess).text( "Your comment is integrated" ).show().fadeOut( 3000 );
                 //find comments scroll div
                 $.post(urlparent, {}, function(data) {
                      var content = $(data).find('.scroll-able.comments-scroll');//TODO chercher le bon scrollable
                      if (content){
                         $(target).html($(content).html());
                      }else{
                         location.reload();
                         return false
                       };
                     });
                 });
                 progress.hide();
        }else{
           var errormessage = '';
           if (intention == ''){
               errormessage =  "intention";
           };
           if (comment == ''){
              if (errormessage != ''){errormessage=errormessage+' and comment'}else{errormessage = 'comment'}
           };
           $( commentmessagedanger).text( "Your "+errormessage+" cannot be empty!" ).show().fadeOut( 4000 );

       };
      event.preventDefault();
   });

});
