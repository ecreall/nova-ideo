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

function init_comment_scroll(){
  var last_child = $('.comments-scroll ul.commentulorigin > .commentli:last-child');
  if (last_child.length > 0){
      var top = last_child.offset().top - $('.comments-scroll').offset().top  + last_child.height() + 10;
      if (top < 700){
       $('.comments-scroll').height(top)
      }
  }else{
       $('.comments-scroll').height(100)
  }
};


$(document).ready(function(){
    init_select_association();
    
     $($('.commentform').parents('.panel').first()).on('shown.bs.collapse', function () {
       init_comment_scroll();
     });
    $(document).on('submit','.commentform', function( event ) {
        var button = $(this).find('button').last();
        var intention = $(this).find("select[name=\'intention\']").select2('val');
        var select_related_contents = $($(this).find("select[name='related_contents']").first());
        var related_contents = get_data(select_related_contents.select2('val'));
        var textarea = $(this).find('textarea');
        var comment = textarea.val();
        var parent = $($(this).parents('.panel-body').first());
        var target = parent.find('.scroll-able.comments-scroll');
        var commentmessageinfo = parent.find('#messageinfo');
        var commentmessagesuccess = parent.find('#messagesuccess');
        var commentmessagedanger = parent.find('#messagedanger');
        var progress = parent.find('#progress');
        var url = $(event.target).data('url');
        if (comment !='' && intention!=''){
          progress.show();// TODO
          $(button).addClass('disabled');
          $( commentmessageinfo).text( novaideo_translate("Comment sent") ).show().fadeOut( 4000 );
          var values = $(this).serialize()+'&'+button.val()+'='+button.val();
          $.post(url, values, function(data) {
                 var content = $(data).find('.scroll-able.comments-scroll');
                 if (content){
                   var label = $($(content).parents(".panel").first()).find('.panel-heading span.action-message').html();
                   $($(target).parents(".panel").first()).find('.panel-heading span.action-message').html(label);
                   $(target).html($(content).html());
                   $( commentmessagesuccess).text( novaideo_translate("Your comment is integrated") ).show().fadeOut( 4000 );
                   textarea.val('');
                   select_related_contents.parents('.controled-form').first().addClass('hide-bloc');
                   $($(select_related_contents.parents('.controled-form').first()).find("input[name='associate']").first()).prop('checked', false);
                   select_related_contents.select2('val', []);
                   init_select_association();
                   init_comment_scroll();
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

        var intention = $(this).find("select[name=\'intention\']").select2('val');
        var textarea = $(this).find('textarea');
        var comment = textarea.val();

        var parent = $($(this).parents('.panel-body').get(1));
        var modal = $(parent).find('.modal.fade:has(form[id|=\''+formid+'\'])');
        var parentform = parent.find('.commentform');
        var urlparent = $(parentform).data('url');

        var target = parent.find('.scroll-able.comments-scroll');
        var commentmessageinfo = parent.find('#messageinfo');
        var commentmessagesuccess = parent.find('#messagesuccess');
        var commentmessagedanger = parent.find('#messagedanger');
        var progress = parent.find('#progress');
        var url = $(event.target).data('url');
        if (comment !='' && intention!=''){
          progress.show();// TODO
          $(modal).modal('hide');
          $( commentmessageinfo).text( novaideo_translate("Comment sent") ).show().fadeOut( 4000 );
          var values = $(this).serialize()+'&'+button.val()+'='+button.val();
          $.post(url, values, function(data) {
                 $( commentmessagesuccess).text( novaideo_translate("Your comment is integrated") ).show().fadeOut( 4000 );
                 $.post(urlparent, {}, function(data) {
                      var content = $(data).find('.scroll-able.comments-scroll');
                      if (content){
                         $(target).html($(content).html());
                         init_select_association();
                         init_comment_scroll()
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
