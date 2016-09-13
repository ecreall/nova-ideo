
function related_item_template(item){
   var markup = '<div class="clearfix">' +
                '<div class="col-sm-1">'
   if(item.icon){
      markup += '<span class=\"search-icon '+item.icon+'\"></span>'
   };
   markup += '</div>'+
             '<div clas="col-sm-10">' +
               '<div class="clearfix">' +
                  '<div class="col-sm-3">' + item.text + '</div>';
   if (item.description) {
      markup += '<div class="col-sm-8">' + item.description + '</div>';
    };
   markup += '</div></div></div>';
   return markup
};



try {
    select2_ajax_templates['related_item_template'] = related_item_template;
}
catch(err) {
}


function replays_show(element){
    var $element = $(element)
    var replays = $($element.parents('li').first().find('ul.commentul:not(.replay-bloc)').first().children('li:not(.comment-preview)'));
    if($(element).hasClass('closed')){
       replays.slideDown( );
       $($element.find('span').first()).attr('class', 'glyphicon glyphicon-chevron-up');
       $element.addClass('opened');
       $element.removeClass('closed');
       $($element.find('.comment-replay-message-closed').first()).removeClass('hide-bloc');
       $($element.find('.comment-replay-message-opened').first()).addClass('hide-bloc');
    }else{
       replays.splice(-1,1);
       replays.slideUp();
       $($element.find('span').first()).attr('class', 'glyphicon glyphicon-chevron-down');
       $element.addClass('closed');
       $element.removeClass('opened');
       $($element.find('.comment-replay-message-closed').first()).addClass('hide-bloc');
       $($element.find('.comment-replay-message-opened').first()).removeClass('hide-bloc');
    }

};


function comment_scroll_to(element, animate){
  var comment_scroll = null 
  var sidebar = $(element.parents('.sidebar-right-wrapper').first())
  if(sidebar.length>0){
      comment_scroll = sidebar
  }
  else{
    comment_scroll = $(element.find('.comments-scroll').first())
  }
 var top = element.position().top-(element.height()+100);       
 // comment_scroll.scrollTop(element.position().top-(element.height()+10));
  comment_scroll.animate({ scrollTop: top}, 1000);
  if (animate){
    var to_animate = $(element.find('.comment-data').first())
    to_animate.animate({
        backgroundColor: "#bca"
      }, 2000 );
    to_animate.animate({
        backgroundColor: "white"
      }, 2000 );
  }
};


//TODO to remove
function init_comment_scroll(element){
  var last_child = null
  var comment_scroll = null 
  var is_sidebar = false
  if (element){
    var sidebar = $(element.parents('.sidebar-right-wrapper').first())
    if(sidebar.length>0){
        comment_scroll = sidebar
        is_sidebar = true
    }
    else{
      comment_scroll = $(element.find('.comments-scroll').first())
    }
    last_child = $(comment_scroll.find('ul.commentulorigin > .commentli:last-child'))
  }else{
     comment_scroll = $('.comments-scroll')
     last_child = $('.comments-scroll ul.commentulorigin > .commentli:last-child');
  }
  if(!is_sidebar){
    if (last_child.length > 0){
        var top = last_child.offset().top - comment_scroll.offset().top  + last_child.height() + 10;
        if (top < 700){
         comment_scroll.height(top)
        }
    }else{
         comment_scroll.height(100)
    }
  }
  var comment_id = '#comment-' + window.location.hash.replace('#comment-', '')
  var elem = $(comment_id);
  if(elem.length) {
     var hide_comment = $(elem.parents('.commentli.hide-bloc'))
     $(hide_comment.parents('.commentli:not(.hide-bloc)').children('.comment-data').find('#commentaction .comment-replay-nb.closed')).click() 
     // var parent = $(elem.parents('.actions-footer-container'))
     setTimeout(function(){comment_scroll_to($(elem.parents('.commentli').first()), true)}, 1000)
  }else{
   // if (comment_scroll.length>0){
     // comment_scroll.animate({ scrollTop: comment_scroll.prop("scrollHeight")}, 1000);
     comment_scroll.scrollTop(comment_scroll.prop("scrollHeight"));
   }
};

function get_form_replay_container(){
  return '<div class=\"replay-form-container\">'+
            '<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>'+
          '</div>'
}

function update_replay(url){
    var $this = $(this)
    $this.parents('.comments-scroll').find('.replay-form-container button.close').click()
    var toreplay = $this.closest('.comment-inline-toggle').data('toreplay');
    var target = $this.closest('.comment-inline-toggle').data('target');
    if (Boolean(toreplay)){$(target).parent('ul.replay-bloc').removeClass('hide-bloc'); return false}
    var url = $this.closest('.comment-inline-toggle').data('updateurl');
    $.getJSON(url,{tomerge:'True', coordinates:'main'}, function(data) {
       var action_body = data['body'];
       if (action_body){
           $($(target).find('.media-body').first()).html(get_form_replay_container());
           var container = $($(target).find('.replay-form-container').first());
           container.append($(action_body));
           init_emoji($(container.find('.emoji-container:not(.emojified)')));
           var replay_bloc = $($(target).parents('ul.replay-bloc').first());
           var commentdata = $(replay_bloc.find('.comment-data').first());
           var commentli = $(replay_bloc.parents('.commentli').first());
           $(container.find('button.close').first()).on('click', function(){
              replay_bloc.css('display', 'none');
              commentdata.removeClass('replay-active')
              commentli.removeClass('replay-active')
           });
           replay_bloc.slideDown()
           commentdata.addClass('replay-active')
           commentli.addClass('replay-active')
           var textareainput = $(replay_bloc.find('textarea').first())
           textareainput.val(textareainput.val()).focus()
           comment_scroll_to(replay_bloc)
           try {
                deform.processCallbacks();
            }
           catch(err) {
            alert(err)
           };
        }else{
           location.reload();
           return false
        }
    });
    return false;
};


function search_comments(input){
  var navchannel = $(input.parents('.navbar-channel'))
  var text_to_search = $(navchannel.find('.comments-text-search').first()).val()
  var filters = $(navchannel.find('.comment-filter-action.active')).map(function(){return $(this).data('name')})
  var commentsscroll = $(navchannel.siblings('.comments-scroll').first())
  var commentscontainer = $(commentsscroll.find('.comments-container').first())
  var comment_ul = $(commentscontainer.find('.commentulorigin').first())
  var next_path = comment_ul.data('origin_url')
  var loading = $(comment_ul.siblings('.comment-loading').first())
  loading_progress()
  $.post(next_path, {filters: filters.toArray(), text: text_to_search}, function(data) {
      var new_comment_ul = $($(data).find('.comments-scroll .comments-container .commentulorigin').first())
      commentscontainer.find('.commentulorigin').remove()
      if(new_comment_ul.length>0){
        loading.addClass('hide-bloc')
        init_emoji($(new_comment_ul.find('.emoji-container:not(.emojified)')));
        commentscontainer.append(new_comment_ul)
      }
      finish_progress()
  })
}


function update_comment(element){
  var url = $('body').data('api_url')
  $.post(url, {op: 'update_comment',
              comment_id: element.data('comment_id')}, function(data){
    if(data.removed){
      element.remove()
      var component = $($('.dace-action-sidebar.activated>span').first())
    }else{
      var content = $(data.body).find('.commentulorigin');
      if (content){
         init_emoji($(content.find('.emoji-container:not(.emojified)')));
         element.replaceWith($($(content).find('li.commentli').first()))
        }
    }     
  })

}

$(document).on('click', '.comment-filter-action', function(){
      var $this = $(this);
      $this.toggleClass('active')
      search_comments($this)
});


$(document).on('change', '.comments-text-search', function(){
      var $this = $(this);
      search_comments($this)
});

$(document).ready(function(){

  $('.sidebar-right-wrapper').on( 'scroll', function(){
      var $this = $(this);
      if($($this.find('.comments-scroll')).length > 0 && $this.scrollTop() <= 0) {
            var navchannel = $($this.find('.navbar-channel'))
            var text_to_search = $(navchannel.find('.comments-text-search').first()).val()
            var filters = $(navchannel.find('.comment-filter-action.active')).map(function(){return $(this).data('name')})
            var commentscontainer = $($this.find('.comments-scroll .comments-container').first())
            var comment_ul = $(commentscontainer.find('.commentulorigin').first())
            var next_path = comment_ul.data('nex_url')
            var loading = $(comment_ul.siblings('.comment-loading').first())
            loading.removeClass('hide-bloc')
            $.post(next_path, {filters: filters.toArray(), text: text_to_search}, function(data) {
                var new_comment_ul = $($(data).find('.comments-scroll .comments-container .commentulorigin').first())
                if(new_comment_ul.length>0){
                  init_emoji($(new_comment_ul.find('.emoji-container:not(.emojified)')));
                  loading.addClass('hide-bloc')
                  new_comment_ul.insertBefore(comment_ul)
                  $this.scrollTop(new_comment_ul.height());
                }else{
                  var comments = $(comment_ul.parents('div').first().find('.commentulorigin > li.commentli:not(.comment-preview)'))
                  if(comments.length > 0){
                    loading.html($('<span class="label label-warning">'+ novaideo_translate("No more item.")+"</span>"))
                  }else{
                    loading.addClass('hide-bloc')
                  }
                }
            })
        }
  });

    $(document).on('click', '.comment-inline-toggle', update_replay);


    $(document).on('submit','.commentform:not(.comment-inline-form)', function( event ) {
        var $this = $(this)
        var button = $this.find('button[type="submit"]').last();
        var select_itention = $($this.find("select[name=\'intention\']"))
        var intention = select_itention.val();
        var select_related_contents = $($this.find("select[name='related_contents']").first());
        var textarea = $this.find('textarea');
        var comment = textarea.val();
        var parent = $($this.parents('.views-container').first());
        var target = $(parent.find('.comments-scroll .commentulorigin'));
        var commentmessageinfo = $this.find('#messageinfo');
        var commentmessagesuccess = $this.find('#messagesuccess');
        var commentmessagedanger = $this.find('#messagedanger');
        var url = $(event.target).attr('action');
        if (comment !='' && intention!=''){
          var preview = $(target.find('> .commentli.comment-preview').last());
          $(preview.find('.comment-preview-text')).html(comment.replace(/\n/g, '</br>'))
          init_emoji($(preview.find('.comment-preview-text')));
          preview.removeClass('hide-bloc')
          init_comment_scroll(parent)
          $(button).addClass('disabled');
          var formData = new FormData($(this)[0]);
          formData.append(button.val(), button.val())
          $( commentmessageinfo).text( novaideo_translate("Comment sent") ).show().fadeOut( 4000 );
          $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                var content = $(data.new_body).find('.commentulorigin');
                if (content){
                   init_emoji($(content.find('.emoji-container:not(.emojified)')));
                   $($(content).find('li.commentli').first()).insertBefore(preview);
                   preview.addClass('hide-bloc')
                   $( commentmessagesuccess).text( novaideo_translate("Your comment is integrated") ).show().fadeOut( 4000 );
                   textarea.val('');
                   select_related_contents.select2('val', []);
                   $($this.find('.comment-files .form-group.deform-seq-item  ')).remove()
                   select_itention.select2('val', 'Remark')
                   init_comment_scroll(parent)
                   try {
                     deform.processCallbacks();
                    }
                   catch(err) {};
                }else{
                 $(commentmessagedanger).text(
                    novaideo_translate("Your comment is not integrated") ).show().fadeOut( 6000 );
                };
                $(button).removeClass('disabled');
                update_components(data)
              }});
              
        }else{
           var errormessage = '';
           if (intention == ''){
              errormessage = 'intention'
            };
           if (textarea.val() == ''){
              if (errormessage != ''){errormessage=errormessage+' and comment'}else{errormessage = 'comment'}
           };
           $( commentmessagedanger).text( "Your "+errormessage+" cannot be empty!" ).show().fadeOut( 4000 );

       };
       event.preventDefault();
   });
  

    $(document).on('submit','.respondform', function( event ) {
        var $this = $(this)
        var formid = $this.attr('id');
        var button = $this.find('button[type="submit"]').last();
        var select_itention = $($this.find("select[name=\'intention\']"))
        var intention = select_itention.val();
        var textarea = $this.find('textarea');
        var comment = textarea.val();
        var select_related_contents = $($this.find("select[name='related_contents']").first());
        var parent = $($this.parents('.views-container').get(1));
        var parentform = parent.find('.commentform');
        
        var target = $($this.parents('.commentli').first().find('.comments-container').first().find('.commentul').first());
        var commentmessageinfo = $this.find('#messageinfo');
        var commentmessagesuccess = $this.find('#messagesuccess');
        var commentmessagedanger = $this.find('#messagedanger');
        var url = $(event.target).attr('action');
        if (comment !='' && intention!=''){
          var preview = $(target.find('> .commentli.comment-preview').last());
          $(preview.find('.comment-preview-text')).html(comment.replace(/\n/g, '</br>'))
          init_emoji($(preview.find('.comment-preview-text')));
          preview.removeClass('hide-bloc')
          comment_scroll_to(preview, true)
          $(button).addClass('disabled');
          $( commentmessageinfo).text( novaideo_translate("Comment sent") ).show().fadeOut( 4000 );
          var formData = new FormData($(this)[0]);
          formData.append(button.val(), button.val())
          $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
              var content = $(data.new_body).find('.commentulorigin');
              if (content){
                 init_emoji($(content.find('.emoji-container:not(.emojified)')));
                 $( commentmessagesuccess).text( novaideo_translate("Your comment is integrated") ).show().fadeOut( 4000 );
                 $($(content).find('li.commentli').first()).insertBefore(preview);
                 preview.addClass('hide-bloc')
                 textarea.val('');
                 select_related_contents.select2('val', []);
                 $($this.find('.comment-files .form-group.deform-seq-item  ')).remove()
                 select_itention.select2('val', 'Remark')
                 $this.parents('.replay-form-container').first().find('button.close').first().click()
                 comment_scroll_to(target.find('> li.commentli:not(.comment-preview)').last(), true)
                 try {
                     deform.processCallbacks();
                    }
                 catch(err) {};
              }else{
                $(commentmessagedanger).text(
                  novaideo_translate("Your comment is not integrated") ).show().fadeOut( 6000 );
              };
              update_components(data)
          }});
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

    $(document).on('submit','.edit-comment-form', function( event ) {
        var $this = $(this)
        var formid = $this.attr('id');
        var button = $this.find('button[type="submit"]').last();
        var select_itention = $($this.find("select[name=\'intention\']"))
        var intention = select_itention.val();
        var textarea = $this.find('textarea');
        var comment = textarea.val();
        var select_related_contents = $($this.find("select[name='related_contents']").first());
        var parent = $($this.parents('.views-container').get(1));
        var parentform = parent.find('.commentform');
        
        var target = $($this.parents('.commentli').first().find('.comments-container').first().find('.commentul').first());
        var commentmessageinfo = $this.find('#messageinfo');
        var commentmessagesuccess = $this.find('#messagesuccess');
        var commentmessagedanger = $this.find('#messagedanger');
        var url = $(event.target).attr('action');
        if (comment !='' && intention!=''){
          $(button).addClass('disabled');
          $( commentmessageinfo).text( novaideo_translate("Comment sent") ).show().fadeOut( 4000 );
          var formData = new FormData($(this)[0]);
          formData.append(button.val(), button.val())
          $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
              var content = $(data.new_body).find('.commentulorigin');
              if (content){
                 init_emoji($(content.find('.emoji-container:not(.emojified)')));
                 $( commentmessagesuccess).text( novaideo_translate("Your comment is integrated") ).show().fadeOut( 4000 );
                 $this.parents('.commentli').first().replaceWith($($(content).find('li.commentli').first()))
                 textarea.val('');
                 select_related_contents.select2('val', []);
                 $($this.find('.comment-files .form-group.deform-seq-item  ')).remove()
                 select_itention.select2('val', 'Remark')
                 $this.parents('.replay-form-container').first().find('button.close').first().click()
                 try {
                     deform.processCallbacks();
                    }
                 catch(err) {};
              }else{
                $(commentmessagedanger).text(
                  novaideo_translate("Your comment is not integrated") ).show().fadeOut( 6000 );
              };
          }});
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


    $(document).on('submit','.presentform', function( event ) {
        var $this = $(this)
        var button = $this.find('button').last();
        var members = $this.find("select[name=\'members\']");
        var subject = $this.find("input[name=\'subject\']").val();
        var textarea = $this.find('textarea');
        var parent = $($this.parents('.views-container').first());
        var target = $(parent.find('.study-view').first());
        var commentmessageinfo = parent.find('#messageinfo');
        var commentmessagesuccess = parent.find('#messagesuccess');
        var commentmessagedanger = parent.find('#messagedanger');
        var url = $(event.target).attr('action');
        if (subject !='' && textarea.val()!='' && members.val() != null){
          loading_progress();
          $(button).addClass('disabled');
          $( commentmessageinfo).text( novaideo_translate("Message sent") ).show().fadeOut( 3000 );
          var values = $this.serialize()+'&'+button.val()+'='+button.val();
          $.post(url, values, function(data) {
                 var content = $(data.new_body).find('.study-view.study-present');
                 if (content){
                  // var label = $($(content).parents(".panel").first()).find('.panel-heading span.action-message').html();
                   // $($(target).parents(".panel").first()).find('.panel-heading span.action-message').html(label);
                   $(target).html($(content).html());
                   members.select2('val', []);
                  $(commentmessagesuccess).text(
                        novaideo_translate("Your message has been delivered to the following recipients") ).show().fadeOut( 6000 );
                  }else{
                    $(commentmessagedanger).text(
                        novaideo_translate("Your message is not delivered") ).show().fadeOut( 6000 );
                  };
                  $(button).removeClass('disabled');
                  update_components(data)
              });
              finish_progress();
        }else{
           var errormessage = '';
           if (members.val() == null){
               errormessage =  "members";
           };
           if (subject == ''){
              if (errormessage != ''){errormessage=errormessage+' and subject'}else{errormessage = 'subject'}
           };
           if (textarea.val() == ''){
              if (errormessage != ''){errormessage=errormessage+' and message'}else{errormessage = 'message'}
           };
           $( commentmessagedanger).text( "Your "+errormessage+" cannot be empty!" ).show().fadeOut( 4000 );

       };
       event.preventDefault();
   });


      $(document).on('click','.commentform .comment-textarea-actions .comment-submit', function(event){
         var $this = $(this)
        var form = $($this.parents('form').first())
        $((".comment-form-group")).removeClass('active')
        var button = $(form.find("button[type='submit']").first());
        button.click()
      });

      $(document).on('click', '.comment-cancel', function(){
        var $this = $(this)
        var form = $($this.parents('form').first())
        $((".comment-form-group")).removeClass('active')
        $((".comment-data .comment-content.hide-bloc")).removeClass('hide-bloc');
        var close_btn = $($(form).parents('.replay-form-container').first().find('button.close').first());
        close_btn.click()
      })
      
      $(document).on('click','.commentform .comment-textarea-actions .comment-intention', function(event){
        var $this = $(this)
        var form = $($this.parents('form').first())
        $((".comment-form-group")).removeClass('active')
        var button = $(form.find(".comment-form-group.comment-intention-form").first());
        button.addClass('active')
        // button.css('bottom', form.offset().top- $(window).height()+'px')
      });

      $(document).on('click','.commentform .comment-textarea-actions .comment-related', function(event){
        var $this = $(this)
        var form = $($this.parents('form').first())
        $((".comment-form-group")).removeClass('active')
        var button = $(form.find(".comment-form-group.comment-related-form").first());
        button.addClass('active')
        // var bottom =($('.comments-scroll').offset().top + $('.comments-scroll').height() - form.offset().top)+70;
        // button.css('bottom', bottom+'px')
      });

      $(document).on('click','.commentform .comment-textarea-actions .comment-add-file', function(event){
        var $this = $(this)
        var form = $($this.parents('form').first())
        $((".comment-form-group")).removeClass('active')
        var button = $(form.find(".comment-form-group.comment-files").first());
        button.addClass('active')
        // button.css('bottom', $this.parents('form').offset().top+'px')
      });

      $(document).on('click','.commentform .comment-textarea textarea', function(event){
        var $this = $(this)
        var form = $($this.parents('form').first())
        $((".comment-form-group")).removeClass('active')
      });

      $(document).on('click','.commentform .comment-textarea-actions .comment-emoji', function(event){
        var $this = $(this)
        var form = $($this.parents('form').first())
        $((".comment-form-group")).removeClass('active')
        var button = $(form.find(".comment-form-group.emoji-container-input").first());
        button.addClass('active')
        // button.css('bottom', $this.parents('form').offset().top+'px')
      });

  $(document).on('click', '.emoji-container-input span.emoji-sizer', function(){
        var $this = $(this)
        var value = ':'+$($this.find('.emoji-inner').first()).attr('title')+':'
        var container = $($this.parents('.emoji-container-input'))
        var text = $(container.siblings('textarea'))
        text.insertAtCaret(value)
        // text.val(text.val()+' '+value+' ')
        container.removeClass('active')

  })

  $(document).on('click', '.comment-ajax-action', function(){
      $('.comment-ajax-action').removeClass('active')
      $(this).addClass('active')
  })

  $(document).on('submit', '.comment-un-pin-form', function(event){
        var $this = $(this)
        var button = $this.find('button.active[type="submit"]').first();
        if(button.val() == 'Cancel'){
          $($this.parents('.modal').first()).modal('hide');
          event.preventDefault();
          return
        }
        var action = $($('.comment-un-pin-action.active').first())
        var url = $(event.target).attr('action');
        $(button).addClass('disabled');
        var formData = new FormData($(this)[0]);
        formData.append(button.val(), button.val())
        $.ajax({
            url: url,
            type: 'POST',
            data:formData,
            contentType: false,
            processData: false,
            success: function(data) {
              var navchannel = $(action.parents('.comments-scroll').first().siblings('.navbar-channel').first())
              var filters = $(navchannel.find('.comment-filter-action.active')).map(function(){return $(this).data('name')})
              filters = filters.toArray()
              if ($.inArray('pinned', filters)>=0){
                //action is unpin with the 'pinned' filter => remove the comment
                $(action.parents('li.commentli').first()).remove()
              }else{
                update_comment($(action.parents('li.commentli').first()))
              }
              $($this.parents('.modal').first()).modal('hide')

          }})

        event.preventDefault();
  })

  $(document).on('submit', '.comment-remove-form', function(event){
        var $this = $(this)
        var button = $this.find('button.active[type="submit"]').first();
        if(button.val() == 'Cancel'){
          $($this.parents('.modal').first()).modal('hide');
          event.preventDefault();
          return
        }
        var action = $($('.comment-remove-action.active').first())
        var url = $(event.target).attr('action');
        $(button).addClass('disabled');
        var formData = new FormData($(this)[0]);
        formData.append(button.val(), button.val())
        $.ajax({
            url: url,
            type: 'POST',
            data:formData,
            contentType: false,
            processData: false,
            success: function(data) {
              update_comment($(action.parents('li.commentli').last()))
              $($this.parents('.modal').first()).modal('hide')
              update_components(data)
          }})

        event.preventDefault();
  })


  $(document).on('submit', '.channel-unsubscribe-form', function(event){
        var $this = $(this)
        var button = $this.find('button.active[type="submit"]').first();
        if(button.val() == 'Cancel'){
          $($this.parents('.modal').first()).modal('hide');
          event.preventDefault();
          return
        }
        var url = $(event.target).attr('action');
        $(button).addClass('disabled');
        var formData = new FormData($(this)[0]);
        formData.append(button.val(), button.val())
        $.ajax({
            url: url,
            type: 'POST',
            data:formData,
            contentType: false,
            processData: false,
            success: function(data) {
              $($this.parents('.modal').first()).modal('hide')
              data.channel_item = $('.channel-action.ajax-action.activated')
              data.removed = true
              update_components(data)
          }})

        event.preventDefault();
  })

  $(document).on('submit', '.channel-subscribe-form', function(event){
        var $this = $(this)
        var button = $this.find('button.active[type="submit"]').first();
        if(button.val() == 'Cancel'){
          $($this.parents('.modal').first()).modal('hide');
          event.preventDefault();
          return
        }
        var url = $(event.target).attr('action');
        $(button).addClass('disabled');
        var formData = new FormData($(this)[0]);
        formData.append(button.val(), button.val())
        $.ajax({
            url: url,
            type: 'POST',
            data:formData,
            contentType: false,
            processData: false,
            success: function(data) {
              $($this.parents('.modal').first()).modal('hide')
              data.channels_target = $($('.channel-action.view-item').first().parents('div').first())
              update_components(data)
          }})
        
        event.preventDefault();
  })

  $(document).on('hidden.bs.modal', '.modal', function(){
        if($('.sidebar-right-background.toggled').length > 0){
          $('body').addClass('modal-open')
        }
   })

   $(document).on('click', '.comment-edit-action', function(){
      $($(this).parents('.commentli').first().find('.comment-data .comment-content').first()).addClass('hide-bloc')
   })  

});
