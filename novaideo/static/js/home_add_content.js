function open_add_content_form(){

  if($('.modal-home-add-content').length == 0){
    $(document.body).append('<div class="modal-backdrop fade in modal-home-add-content"></div>')
  }
  var add_content_form = $(".home-add-content")
  add_content_form.css("position","relative");
  add_content_form.find(".form-group:not(.content-preview-form),"+
     ".form-group label,"+
     ".form-group.content-preview-form #desc").slideDown();
  add_content_form.addClass('opened').removeClass('closed')
}

function close_add_content_form(){
  var add_content_form = $(".home-add-content")
  add_content_form.css("position","inherit");
  var form_groups = add_content_form.find('.form-group')
  form_groups.removeClass('has-error')
  form_groups.find('p.help-block.help-error').remove()
  $('.modal-home-add-content').remove()
  add_content_form.find(".form-group:not(.content-preview-form),"+
     ".form-group label,"+
     ".form-group.content-preview-form #desc").slideUp();
  add_content_form.addClass('closed').removeClass('opened')
  $(".similar-contents.modal").modal('hide')
  add_content_form.find(".btn").removeClass('active')
}

$(document).mouseup(function (e){
    var container = $(".home-add-content, .select2-results");
    if (!container.is(e.target) // if the target of the click isn't the container...
        && container.has(e.target).length === 0
        && $(e.target).parents('body').length != 0) // ... nor a descendant of the container
    {
        if(!$(".home-add-content .form-group.content-preview-form textarea").val()){
           close_add_content_form()
        }
    }
});

$(document).on('change','.home-add-content form input[name="title"], .home-add-content form select[name="keywords"]', function( event ) {
    var $this = $(this)
    var form = $($this.parents('form').first())
    var title = form.find('input[name="title"]').val();
    var keywords = $(form.find('select[name="keywords"]')).val();
    if ((!title || title == '') && (!keywords || keywords.length == 0)){
      event.preventDefault();
      return
    }
    var target = form.parents('.home-add-content').first().find('.similar-contents');
    var url = form.parents('.home-form-container').first().data('url_search')
    $.getJSON(url,{title: title, keywords: keywords}, function(data){
        if(data.body){
          $(target.find('.similar-contents-container').first()).html(data.body)
          target.modal('show')
        }else{
          target.modal('hide')
        }
    });
   event.preventDefault();
});

$(document).on('submit','.home-add-content .home-add-idea form', function( event ) {
    var $this = $(this)
    if($this.hasClass('pending')){
      event.preventDefault();
      return
    }
    $this.addClass('pending')
    var button = $($this.find('button.active').first())
    button.addClass('disabled')
    if(button.val() == 'Cancel'){
      $this.find('textarea[name="text"]').val('');
      $this.find('.deform-close-button').click()
      button.removeClass('active');
      button.removeClass('disabled');
      $this.removeClass('pending')
      close_add_content_form()
      event.preventDefault();
       return
    }
    var parent = $($this.parents('.home-form-container').first());
    var title = $this.find('input[name="title"]').val();
    var text = $this.find('textarea[name="text"]').val();
    var keywords = $($this.find('select[name="keywords"]')).val();
    if(title=='' || text=='' || !keywords || keywords.length == 0){
      var form_groups = $this.find('.form-group')
      form_groups.removeClass('has-error')
      form_groups.find('p.help-block.help-error').remove()
      var input = null;
      var error_help = '<p class="help-error help-block">'+novaideo_translate("Required") +'</p>'
      alert_component({
        alert_msg: novaideo_translate("There was a problem with your submission."),
        alert_type: 'error'
      })
      if (title=='')
      {
        form_group = $this.find('input[name="title"]').parents('.form-group').first()
        form_group.addClass('has-error')
        form_group.append($(error_help))
      }
      
      if (text=='')
      {
         form_group = $this.find('textarea[name="text"]').parents('.form-group').first()
         form_group.addClass('has-error')
         form_group.append($(error_help))
      }

      if (!keywords || keywords.length == 0)
      {
         form_group = $this.find('select[name="keywords"]').parents('.form-group').first()
         form_group.addClass('has-error')
         form_group.append($(error_help))
      }
      button.removeClass('active');
      button.removeClass('disabled');
      $this.removeClass('pending')
      event.preventDefault();
      return
    }
    
    var formData = new FormData($(this)[0]);
    formData.append(button.val(), button.val())
    var action_metadata = get_action_metadata(button)
    for(key in action_metadata){
        formData.append(key, action_metadata[key])
    }
    var url = parent.data('url')
    var buttons = $($this.find('button'))
    buttons.addClass('disabled');
    loading_progress()
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
          var redirect_url = data.redirect_url && !data.ignore_redirect
          if(data.status && !redirect_url){
            var item_target = data.item_target
            $(data.new_obj_body).hide().prependTo($('#'+item_target+' .result-container')).fadeIn(1500)
          }
          $this.find('input[name="title"]').val(data['new_title']);
          $this.find('textarea[name="text"]').val('');
          $this.find('.deform-close-button').click()
          buttons.removeClass('disabled');
          button.removeClass('active');
          $this.removeClass('pending')
          close_add_content_form()
          update_components(data)
          if(!redirect_url){
              finish_progress()
          }
         }
    });
   event.preventDefault();
});


$(document).on('submit','.home-add-content .home-add-question form', function( event ) {
    var $this = $(this)
    if($this.hasClass('pending')){
      event.preventDefault();
      return
    }
    $this.addClass('pending')
    var button = $($this.find('button.active').first())
    button.addClass('disabled')
    if(button.val() == 'Cancel'){
      $this.find('textarea[name="text"]').val('');
      $this.find('.deform-close-button').click()
      button.removeClass('active');
      button.removeClass('disabled');
      $this.removeClass('pending')
      close_add_content_form()
      event.preventDefault();
       return
    }
    var parent = $($this.parents('.home-form-container').first());
    var title = $this.find('input[name="question"]').val();
    var keywords = $($this.find('select[name="keywords"]')).val();
    if(title=='' || !keywords || keywords.length == 0){
      var form_groups = $this.find('.form-group')
      form_groups.removeClass('has-error')
      form_groups.find('p.help-block.help-error').remove()
      var input = null;
      var error_help = '<p class="help-error help-block">'+novaideo_translate("Required") +'</p>'
      alert_component({
        alert_msg: novaideo_translate("There was a problem with your submission."),
        alert_type: 'error'
      })
      if (title=='')
      {
        form_group = $this.find('input[name="question"]').parents('.form-group').first()
        form_group.addClass('has-error')
        form_group.append($(error_help))
      }

      if (!keywords || keywords.length == 0)
      {
         form_group = $this.find('select[name="keywords"]').parents('.form-group').first()
         form_group.addClass('has-error')
         form_group.append($(error_help))
      }
      button.removeClass('active');
      button.removeClass('disabled');
      $this.removeClass('pending')
      event.preventDefault();
      return
    }
    
    var formData = new FormData($(this)[0]);
    formData.append(button.val(), button.val())
    var action_metadata = get_action_metadata(button)
    for(key in action_metadata){
        formData.append(key, action_metadata[key])
    }
    var url = parent.data('url')
    var buttons = $($this.find('button'))
    buttons.addClass('disabled');
    loading_progress()
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
          var redirect_url = data.redirect_url && !data.ignore_redirect
          if(data.status && !redirect_url){
            var item_target = data.item_target
            $(data.new_obj_body).hide().prependTo($('#'+item_target+' .result-container')).fadeIn(1500)
          }
          $this.find('input[name="question"]').val('');
          $this.find('textarea[name="text"]').val('');
          $this.find('.deform-close-button').click()
          buttons.removeClass('disabled');
          button.removeClass('active');
          $this.removeClass('pending')
          close_add_content_form()
          update_components(data)
          if(!redirect_url){
              finish_progress()
          }
         }
    });
   event.preventDefault();
});

$(document).ready(function(){

  $('.home-add-content.closed  span.form-icon').on('click', function(){
      $(this).siblings('div.content-form').find('.content-preview-form textarea').click().focus();
  })

  $(".home-add-content.closed .form-group.content-preview-form").click(function(e) {
      open_add_content_form()
  });

  $(".home-content-nav>li>a").click(function(e) {
	  var add_content_form = $(".home-add-content") 
	  var container = add_content_form.parents('.home-add-content-container').first()
	  var content_id = $(this).data('content_id')
	  container.attr('class', content_id+' home-add-content-container')
  });

});