function get_data(selecteds){
    var selecteds = jQuery.makeArray(selecteds);
    var result= [];
    for(i=0;i<selecteds.length; i++){
       result[i] = selecteds[i].id
    };
    return result
};

function init_select_association(){
    $('.select-associations').click(function(){
        var comments = $($($($(this).parents('.comments-scroll').first()).find('ul.commentulorigin').first()).children().filter("li[data-association='false']"));
        if (this.checked) {
            comments.addClass('hide-bloc')            
        }else{
           comments.removeClass('hide-bloc')
        }
    });
};

function replays_show(element){
    var replays = $($($(element).parents('li').first()).find('ul').first());
    if(replays.hasClass('hide-bloc')){
       replays.removeClass('hide-bloc');
       $($(element).find('span').first()).attr('class', 'glyphicon glyphicon-chevron-up');
    }else{
       replays.addClass('hide-bloc');
       $($(element).find('span').first()).attr('class', 'glyphicon glyphicon-chevron-down');
    }

};

$(document).ready(function(){
    init_select_association();

    $(document).on('submit','.commentform', function( event ) {
        var button = $(this).find('button').last();
        var intention = $(this).find('.select2-chosen').text();
        var select_related_contents = $($(this).find("select[name='related_contents']").first());
        var related_contents = get_data(select_related_contents.select2('data'));
        var textarea = $(this).find('textarea');
        var comment = textarea.val();
        var parent = $($(this).parents('.panel-body').first());
        var target = parent.find('.scroll-able.comments-scroll');
        var commentmessageinfo = parent.find('#messageinfo');
        var commentmessagesuccess = parent.find('#messagesuccess');
        var commentmessagedanger = parent.find('#messagedanger');
        var progress = parent.find('#progress');
        var url = $(event.target).data('url');
        if (comment !='' && intention!='- Select -'){
          progress.show();// TODO
          $(button).addClass('disabled');
          $( commentmessageinfo).text( "Comment sent" ).show().fadeOut( 1000 );
          var values = $(this).serialize()+'&'+button.val()+'='+button.val();
          $.post(url, values, function(data) {
                 var content = $(data).find('.scroll-able.comments-scroll');
                 if (content){
                   var label = $($(content).parents(".panel").first()).find('.panel-heading span.label').text();
                   $($(target).parents(".panel").first()).find('.panel-heading span.label').text(label);
                   $(target).html($(content).html());
                   $( commentmessagesuccess).text( "Your comment is integrated" ).show().fadeOut( 3000 );
                   textarea.val('');
                   select_related_contents.parents('.controled-form').first().addClass('hide-bloc');
                   $($(select_related_contents.parents('.controled-form').first()).find("input[name='associate']").first()).prop('checked', false);
                   select_related_contents.select2('data', []);
                   init_select_association();
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
  


    $('.commentform .control-form-button').on('click', function(event){
        var form = $($(this).parents('.ajax-form').find(".controled-form").first());
        var associate = $(form.find("input[name='associate']").first());
        if(!form.hasClass('hide-bloc')){
            associate.prop('checked', true)
        }else{
            associate.prop('checked', false)
        }
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
                         init_select_association();
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
