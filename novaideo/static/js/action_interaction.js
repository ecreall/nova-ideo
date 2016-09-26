
function get_action_metadata(action){
    var id = action.attr('id')
    search_item = $($('[id="'+id+'"]').parents('.result-item.search-item').first())
    var counters = $('.counter').map(function(){return $(this).attr('id')}).get()
    return {source_path: window.location.pathname,
            is_listing: search_item.length > 0,
            search_item: search_item,
            counters: JSON.stringify(counters)}
}


function update_modal_action(event){
    var action = $(this).closest('.dace-action-modal')
    var toreplay = action.data('toreplay');
    var title = action.data('view_title');
    var modal_css_class = action.data('component_style');
    var after_exe_url = action.data('after_exe_url');
    var modal_container = $('.action-modal-container')
    modal_container.attr('class', modal_css_class+' action-modal-container modal fade')
    modal_container.data('after_exe_url', after_exe_url)
    if (Boolean(toreplay)){
      var action_body =jQuery.parseJSON(action.data('body'));
      if($(action_body).hasClass('pontus-main-view')){
         var panel = $($(action_body).find('>.panel-body').first())
         $(modal_container.find('.modal-body')).html(panel.html())
      }else{
          $(modal_container.find('.modal-body')).html(action_body);
      }
      $(modal_container.find('.modal-title')).text(title)
      try {
         deform.processCallbacks();
      }catch(err) {};
      modal_container.modal('show');
      return false
    }
    var url = action.data('updateurl');
    modal_container.css('opacity', '0')
    loading_progress()
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    delete url_attr.search_item;
    $.getJSON(url, url_attr, function(data) {
       var action_body = data['body'];
       if (action_body){
           $(modal_container.find('.modal-body')).html(action_body);
           $(modal_container.find('.modal-title')).text(title)
           modal_container.css('opacity', '1')
           modal_container.modal('show');
           try {
                deform.processCallbacks();
            }
           catch(err) {};
           finish_progress()
           focus_on_form(modal_container)
           modal_container.data('action_id', action.attr('id'))
           return false
        }else{
           location.reload();
           return false
        }
    });
    return false;
};


function update_direct_action(event){
    var action = $(this).closest('.dace-action-direct')
    var id = action.attr('id')
    search_item = $($('[id="'+id+'"]').parents('.result-item.search-item').first())
    var url = action.data('updateurl');
    loading_progress()
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    var search_item = url_attr.search_item
    delete url_attr.search_item;
    $.getJSON(url, url_attr, function(data) {
       data.search_item = search_item
       update_components(data)
       if(!data.redirect_url){
         finish_progress()
       }
       return false
    });
    return false;
};


function update_inline_action(){
    var $this = $(this)
    var target = $($this.parents('.search-item, .content-view').find('.actions-footer-container').first())//closest('.dace-action-inline').data('target')+'-target';
    var actions = $($this.parents('.actions-block').find('.dace-action-inline'));
    if($this.hasClass('activated')){
       target.slideUp();
       actions.removeClass('activated')
       return
    }
    actions.removeClass('activated')
    var action = $this.closest('.dace-action-inline')
    var url = action.data('updateurl');
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    delete url_attr.search_item;
    $.getJSON(url,{tomerge:'True', coordinates:'main',
                   source_path: window.location.pathname}, function(data) {
       var action_body = data['body'];
       if (action_body){
           target.slideDown();
           $(target.find('.container-body')).html(action_body);
           $this.addClass('activated')
           init_comment_scroll(target)
           try {
                deform.processCallbacks();
            }
           catch(err) {};
           focus_on_form(target)
        }else{
           location.reload();
           return false
        }
    });
    return false;
};

function _get_side_bar_title(data){
  var result = '<div class="view-item-title">'
  if (data.img){
    result += '<img class="img-circle" src="'+data.img+'" width="25">'
  }
  else if(data.icon){
    result += '<span class="icon '+data.icon+'"></span>'
  }
   result += ' <span>'+data.title+'</span></div>'
  return result
}


function update_sidebar_action(){
    var $this = $(this)
    var actions = $('.dace-action-sidebar');
    if($this.hasClass('activated')){
       actions.removeClass('activated')
       return
    }
    var sidebar = $('.sidebar-right-nav')
    var bar = $(".bar-right-wrapper")
    var closed = bar.hasClass('toggled')
    
    var target = $(sidebar.find('.actions-footer-container'))//closest('.dace-action-inline').data('target')+'-target';
    var toggle = $('.menu-right-toggle:not(.close)')
    var title = $($this.parents('.view-item, .content-view').first().find('.view-item-title, .content-title').first()).clone()
    actions.removeClass('activated')
    var action = $this.closest('.dace-action-sidebar')
    var url = action.data('updateurl');
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    delete url_attr.search_item;
    loading_progress()
    $.getJSON(url, url_attr, function(data) {
       var action_body = data['body'];
       if (action_body){
          var container_bodu = $(target.find('.container-body'))
           container_bodu.html(action_body);
           if(title.length > 0){
            var new_title = _get_side_bar_title({
               title: title.data('title'),
               img: title.data('img'),
               icon: title.data('icon'),
            })
            $(sidebar.find('.sidebar-title .entity-title').first()).html(new_title)
           }
           $this.addClass('activated')
           try {
                deform.processCallbacks();
            }
           catch(err) {};
           if(toggle.length>0 && closed){
              toggle.click()
           }
           init_emoji($(target.find('.emoji-container:not(.emojified)')));
           rebuild_scrolls($(target.find('.malihu-scroll')))
           init_comment_scroll(target)
           finish_progress()
           focus_on_form(target)
        }else{
           location.reload();
           return false
        }
    });
    return false;
};

function update_popover_action(){
    var $this = $(this)
    var actions = $('.dace-action-popover');
    if($this.hasClass('activated')){
       actions.removeClass('activated')
       return
    }
    var popover_container = $('.action-popover-container')
    var target = $(popover_container.find('.popover-content'))//closest('.dace-action-inline').data('target')+'-target';
    actions.removeClass('activated')
    var action = $this.closest('.dace-action-popover')
    var url = action.data('updateurl');
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    delete url_attr.search_item;
    loading_progress()
    $.getJSON(url, url_attr, function(data) {
       var action_body = data['body'];
       if (action_body){
           target.html(action_body);
           init_emoji($(target.find('.emoji-container:not(.emojified)')));
           rebuild_scrolls($(target.find('.malihu-scroll')))
           $this.addClass('activated')
           var position = $this.offset()
           popover_container.css('top', position.top-$(document).scrollTop()-(popover_container.height()/2)+'px')
           popover_container.css('left', position.left+$this.width()-2+'px')
           popover_container.css('display', 'block')
           popover_container.addClass('in')
           try {
                deform.processCallbacks();
            }
           catch(err) {};
           init_comment_scroll(target)
           finish_progress()
           focus_on_form(target)
        }else{
           location.reload();
           return false
        }
    });
    return false;
};


$(document).on('click', '.dace-action-sidebar', update_sidebar_action);

$(document).on('click', '.dace-action-popover', update_popover_action);

$(document).on('click', 'a.dace-action-modal', update_modal_action);

$(document).on('click', '.dace-action-direct', update_direct_action);


$(document).on('submit', 'form.novaideo-ajax-form', function(event){
    var $this = $(this)
    var formid = $this.attr('id');
    var button = $this.find('button.active[type="submit"]').last();
    var modal_container = $('.action-modal-container.in')
    if(button.val() == 'Cancel'){
      modal_container.modal('hide');
      event.preventDefault();
      return
    }
    var url = $(event.target).attr('action');
    $(button).addClass('disabled');
    var formData = new FormData($(this)[0]);
    formData.append(button.val(), button.val())
    var action = $('#'+modal_container.data('action_id'))
    var action_metadata = get_action_metadata(action)
    var search_item = action_metadata.search_item
    delete action_metadata.search_item;
    for(key in action_metadata){
        formData.append(key, action_metadata[key])
    }
    loading_progress()
    $.ajax({
      url: url,
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function(data) {
        if(data.new_body){
         $this.parents('.views-container').first().html($(jQuery.parseJSON(data.new_body)))
         try {
                deform.processCallbacks();
          }catch(err) {};
         finish_progress()
        }else if(! data.redirect_url){
          modal_container.modal('hide')
          finish_progress()
        }
        data.search_item = search_item
        update_components(data)
    }});
    event.preventDefault();
})


$(document).on('click', function(event){
       var popover_container = $($(event.target).parents('.action-popover-container'))
       if(popover_container.length == 0){
          var active_popover = $('.action-popover-container.in')
          if (active_popover.length >= 1){
            $('.dace-action-popover').removeClass('activated');
            active_popover.css('display', 'none')
            active_popover.removeClass('in')
            $(active_popover.find('.popover-content')).html('');
          }
       }
    });
             