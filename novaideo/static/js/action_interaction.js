
function get_action_metadata(action){
    var id = action.attr('id')
    var view_name = $(document.body).data('view_name')
    var actions = id? $('[id="'+id+'"]'): $(action)
    var object_views = actions.map(function(index){
      var view = $($(this).parents('.component-obj-view.component-listing-view, .component-obj-view.component-index-view').first())
      return view.attr('id')
    }).get()
    var counters = $('[data-component_type="tab_component"], [data-component_type="navbar_component"], [data-component_type="novaideo_content_nb"]')
        .map(function(){return $(this).attr('id')}).get()
    var contextual_help = $('[data-component_type="contextual-help"]').map(function(){return $(this).attr('id')}).get()
    var steps_navbars = $('[data-component_type="process_steps"]').map(function(){return $(this).attr('id')}).get()
    return {source_path: window.location.pathname,
            view_name: view_name,
            object_views: JSON.stringify(object_views),
            counters: JSON.stringify(counters),
            included_resources: JSON.stringify(includejs_resources),
            contextual_help: JSON.stringify(contextual_help),
            steps_navbars: JSON.stringify(steps_navbars),
            load_view: 'load'}
}


function load_views(){
  var body = $(document.body)
  var loading_components = $('[data-component_type="on-load-view"]')
        .map(function(){return $(this).attr('id')}).get()
  data = {
    source_path: window.location.pathname,
    view_name: body.data('view_name'),
    'loading_components': JSON.stringify(loading_components),
    included_resources: JSON.stringify(includejs_resources),
    'op': 'load_views',
    'load_view': 'load'
  }
  var url = body.data('api_url')
  $.post(url, data, function(data) {
    include_resources(data['resources'], function(){
         update_components(data)
    })
  });
}


function update_modal_action(event){
    var action = $(this).closest('.dace-action-modal')
    var toreplay = action.data('toreplay');
    var title = action.data('view_title');
    var modal_css_class = action.data('component_style');
    var after_exe_url = action.data('after_exe_url');
    var modal_container = $('.action-modal-container')
    modal_container.attr('class', modal_css_class+' action-modal-container action-interation-container modal fade')
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
      }
      catch(err) {};
      modal_container.modal('show');
      return false
    }
    var url = action.data('updateurl');
    modal_container.css('opacity', '0')
    loading_progress()
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    $.post(url, url_attr, function(data) {
        include_resources(data['resources'], function(){
           var action_body = data['body'];
           if (action_body){
             $(modal_container.find('.modal-body')).html(action_body);
             $(modal_container.find('.modal-title')).text(title)
             modal_container.css('opacity', '1')
             modal_container.modal('show');
             modal_container.find('.carousel').carousel()
             try {
                  deform.processCallbacks();
             }catch(err) {};
             finish_progress()
             focus_on_form(modal_container)
             modal_container.data('action_id', action.attr('id'))
             init_emoji($(modal_container.find('.emoji-container:not(.emojified)')));
             return false
          }else{
             location.reload();
             return false
          }
        })
     });
    return false;
};


function update_direct_action(event){
    var action = $(this).closest('.dace-action-direct')
    var url = action.data('updateurl');
    loading_progress()
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    $.post(url, url_attr, function(data) {
       update_components(data)
       if(!(data.redirect_url && !data.ignore_redirect)){
         finish_progress()
       }
       return false
    });
    return false;
};


function update_inline_action(){
    var $this = $(this)
    var target = $($this.parents('.search-item').find('.action-inline-container').first())
    if (target.length==0){
      target = $($this.parents('.content-view').find('.action-inline-container').first())
    }
    var actions = $($this.parents('.actions-block').find('.dace-action-inline'));
    if($this.hasClass('activated')){
       target.slideUp();
       actions.removeClass('activated')
       return
    }
    actions.removeClass('activated')
    var action = $this.closest('.dace-action-inline')
    var toreplay = action.data('toreplay');
    if (Boolean(toreplay)){
      var action_body =jQuery.parseJSON(action.data('body'));
      if($(action_body).hasClass('pontus-main-view')){
         var panel = $($(action_body).find('>.panel-body').first())
         $(target.find('.container-body')).html(panel.html())
      }else{
          $(target.find('.container-body')).html(action_body);
      }
      try {
         deform.processCallbacks();
      }
      catch(err) {};
      return false
    }
    
    var url = action.data('updateurl');
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    loading_progress()
    $.post(url, url_attr, function(data) {
      include_resources(data['resources'], function(){
       var action_body = data['body'];
       if (action_body){
           target.slideDown("fast");
           $(target.find('.container-body')).html(action_body);
           $this.addClass('activated')
           target.find('.carousel').carousel()
           try {
                deform.processCallbacks();
            }
           catch(err) {};
           finish_progress()
           target.data('action_id', action.attr('id'))
           focus_on_form(target)
           init_emoji($(target.find('.emoji-container:not(.emojified)')));
        }else{
           location.reload();
           return false
        }
     })
    });
    return false;
};


function _close_slider(slider){
  slider.find('.container-body').css({
      display: 'none'})
 slider.stop().animate({
      width: 0,   
  }, 400, function(){
    slider.css({
      height: 0,
      display: 'none'})
  });
 $(slider.find('.container-body')).html("");
 var id = slider.data('action_id')
 $('[id="'+id+'"]').removeClass('activated')
}


function update_slider_action(){
    var $this = $(this)
    var item = $this.parents('.search-item').first();
    var target = $(item.find('>.action-slider-container').first())
    var is_content_view = false;
    if (target.length==0){
      item = $this.parents('.content-view').first()
      is_content_view = true;
      target = $(item.find('>.action-slider-container').first())
    }
    var is_sidebar = item.parents('.sidebar-container').length>0
    var actions = $($this.parents('.actions-block').find('.dace-action-slider'));
    if($this.hasClass('activated')){
       actions.removeClass('activated');
       _close_slider(target)
       return
    }
    actions.removeClass('activated')
    var action = $this.closest('.dace-action-slider')
    var toreplay = action.data('toreplay');
    if (Boolean(toreplay)){
      var action_body =jQuery.parseJSON(action.data('body'));
      if($(action_body).hasClass('pontus-main-view')){
         var panel = $($(action_body).find('>.panel-body').first())
         $(target.find('.container-body')).html(panel.html())
      }else{
          $(target.find('.container-body')).html(action_body);
      }
      try {
         deform.processCallbacks();
      }
      catch(err) {};
      return false
    }
    
    var url = action.data('updateurl');
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    loading_progress()
    $.post(url, url_attr, function(data) {
      include_resources(data['resources'], function(){
       var action_body = data['body'];
       if (action_body){
          var width = is_content_view? item.outerWidth()+30:item.outerWidth();
          width = is_sidebar && is_content_view? width-10: width;
          var height = is_content_view? item.outerHeight()+15:item.outerHeight();
          target.css({
            height: height,
            display: 'block'})
          target.stop().animate({
              width: width,
          }, 400, function(){
             target.find('.container-body').css({
              display: 'block'})
             $(target.find('.container-body')).html(action_body);
            
             $this.addClass('activated')
             target.find('.carousel').carousel()
             try {
                  deform.processCallbacks();
              }
             catch(err) {};
             target.data('action_id', action.attr('id'))
             init_emoji($(target.find('.emoji-container:not(.emojified)')));
             init_content_text_scroll(target.find(".content-text-scroll"))
             var result_scroll = target.find(".result-scroll")
             var height_scroll = is_content_view && is_sidebar? $(window).height()-30:item.outerHeight()-30
             initscroll(result_scroll)
             rebuild_scrolls(target.find('.malihu-scroll'))
             finish_progress()
             focus_on_form(target)
           });
        }else{
           location.reload();
           return false
        }
     })
    });
    return false;
};

function close_slider_action(){
  var target = $($(this).parents('.action-slider-container').first())
  _close_slider(target)
}



function _update_sidebar_nav_items(target){
  var current_items = $(target.find('.sidebar-container-item'))
  var sidebar_state = current_items.length<=1? 'closed': ''
  var result = '<div class="sidebar-nav-items desabled '+sidebar_state+'">'
  current_items.each(function(){
    var $this = $(this)
    var title = $this.data('title') + ': '+$this.data('context_title')
    var item_state = $this.hasClass('closed')? 'closed': ''
    result += '<div title=\''+title +'\''
    result += ' data-target="'+$this.attr('id')+'"'+
              ' data-scroll="'+$this.data('scroll')+'"'+
              ' class="item '+item_state+'"><span class="'+
              $this.data('icon')+'"></span> '+title+'</div>'
  })
  result += '<span class="item-activator desabled glyphicon glyphicon-th"></span>'
  result += '</div>'
  var current_nav_items = target.find('.sidebar-nav-items')
  if(current_nav_items.length>0){
    current_nav_items.replaceWith(result)
  }else{
    target.append(result)
  }
}


function _wrap_action_body(action, body){
  var title = $(action.parents('.view-item, .content-view').first().find('.view-item-title, .content-title').first())
  return '<div id="sidebar-'+action.attr('id')+'"'+
             ' data-title="'+action.data('title')+'"'+
             ' data-icon="'+action.data('icon')+'"'+
             ' data-context_title=\''+ title.data('title')+'\''+
             ' data-context_icon="'+title.data('icon')+'"'+
             ' data-context_img="'+title.data('img')+'"'+
         'class="sidebar-container-item">' + body + '</div>'
          

}

function open_sidebar_container_item(to_open, interaction_args){
  var new_title = get_component_title({
     title: to_open.data('context_title'),
     img: to_open.data('context_img'),
     icon: to_open.data('context_icon'),
  })
  var sidebar = $('.sidebar-right-nav')
  $(sidebar.find('.sidebar-title .entity-title').first()).html(new_title)
  var current_item = $('.sidebar-nav-items .item:not(.closed)').first();
  var scrollTop = $('.sidebar-right-wrapper').scrollTop()+1;
  current_item.data('scroll', scrollTop)
  current_item.attr('data-scroll', scrollTop)
  var item = $('.sidebar-nav-items .item[data-target="'+to_open.attr('id')+'"]')
  $('.sidebar-nav-items .item').not(item).addClass('closed')
  item.removeClass('closed')
  var current_scroll = item.data('scroll')
  function complete() {
    $(this).addClass('closed')
    to_open.fadeIn("fast").promise().done(
      function(){
        $(this).removeClass('closed');
        if(interaction_args && interaction_args.scroll_bottom){
           init_comment_scroll(sidebar)
        }else if(current_scroll){
            $('.sidebar-right-wrapper').scrollTop(current_scroll);
        }
      })
  }
  $('.sidebar-container-item').fadeOut( "fast").promise().done(complete)
}

function update_sidebar_action(){
    var $this = $(this)
    var actions = $('.dace-action-sidebar');
    if($this.hasClass('activated')){
       actions.removeClass('activated')
       return
    }
    var sidebar = $('.sidebar-right-nav')
    var closed = $(".bar-right-wrapper").hasClass('toggled')
    var target = $(sidebar.find('.sidebar-container'))//closest('.dace-action-inline').data('target')+'-target';
    var toggle = $('.menu-right-toggle:not(.close)')
    var title = $($this.parents('.view-item, .content-view').first().find('.view-item-title, .content-title').first())
    actions.removeClass('activated')
    var action = $this.closest('.dace-action-sidebar')
    var url = action.data('updateurl');
    var interaction_args = action.data('interaction_args')
    var scroll_bottom = interaction_args?interaction_args.indexOf('scroll-bottom') !== -1: false
    var url_attr = {tomerge:'True', coordinates:'main'}
    $.extend( url_attr, get_action_metadata(action));
    loading_progress()
    $.post(url, url_attr, function(data) {
      include_resources(data['resources'], function(){
        var action_body = data['body'];
        if (action_body){
           var container_body = $(target.find('>.container-body').first())
           var wrapped = _wrap_action_body(action, action_body)
           var current_item = null
           if(closed){
             container_body.html(wrapped);
           }else{
             current_item = $(container_body.find('#sidebar-'+action.attr('id')+''))
             if(current_item.length>0){
               current_item.html(action_body)
             }else{
               container_body.append($(wrapped).addClass('closed'));
               current_item = $(container_body.find('#sidebar-'+action.attr('id')+''))
             }
           }
           _update_sidebar_nav_items(container_body)
           if(current_item){
             //first call : put interaction args
             open_sidebar_container_item(current_item, {'scroll_bottom': scroll_bottom})
           }else if(title.length > 0){
             var new_title = get_component_title({
               title: title.data('title'),
               img: title.data('img'),
               icon: title.data('icon'),
             })
             $(sidebar.find('.sidebar-title .entity-title').first()).html(new_title)
             if(scroll_bottom){init_comment_scroll(target)}
           }
           try {
                deform.processCallbacks();
            }
           catch(err) {};
           if(toggle.length>0 && closed){
              toggle.click()
           }
           $this.addClass('activated')
           target.find('.carousel').carousel()
           init_emoji(target.find('.emoji-container:not(.emojified)'));
           init_content_text_scroll(target.find(".content-text-scroll"))
           rebuild_scrolls(target.find('.malihu-scroll'))
           var result_scroll = target.find(".result-scroll")
           initscroll(result_scroll)
           finish_progress()
           focus_on_form(target)
        }else{
           location.reload();
           return false
        }
      })
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
    $.extend(url_attr, get_action_metadata(action));
    loading_progress()
    $.post(url, url_attr, function(data) {
      include_resources(data['resources'], function(){
       var action_body = data['body'];
       if (action_body){
           target.html(action_body);
           $this.addClass('activated')
           var position = $this.offset()
           popover_container.css('top', position.top-$(document).scrollTop()-(popover_container.height()/2)+'px')
           .css('left', position.left+$this.width()-2+'px')
           .css('display', 'block')
           .addClass('in')
           try {
                deform.processCallbacks();
            }
           catch(err) {};
           target.find('.carousel').carousel()
           init_emoji(target.find('.emoji-container:not(.emojified)'));
           init_content_text_scroll(target.find(".content-text-scroll"))
           rebuild_scrolls(target.find('.malihu-scroll'))
           var result_scroll = target.find(".result-scroll")
           initscroll(result_scroll)
           finish_progress()
           focus_on_form(target)
           target.data('action_id', action.attr('id'))
        }else{
           location.reload();
           return false
        }
      })
    });
    return false;
};

$(document).on('click', '.dace-action-sidebar', update_sidebar_action);

$(document).on('click', '.dace-action-popover', update_popover_action);

$(document).on('click', '.dace-action-modal', update_modal_action);

$(document).on('click', '.dace-action-direct', update_direct_action);

$(document).on('click', '.dace-action-inline', update_inline_action);

$(document).on('click', '.dace-action-slider', update_slider_action);
$(document).on('click', '.action-slider-btn', close_slider_action);



function hide_action_interaction_container(action_container){
  var interaction_type = action_container.data('interaction_kind');
  if(interaction_type == 'modal'){action_container.modal('hide');}
  if(interaction_type == 'inline'){action_container.slideDown();}
  if(interaction_type == 'popover'){action_container.css('display', 'none');}
  if(interaction_type == 'slider'){_close_slider(action_container)}
}


$(document).on('submit', 'form.novaideo-ajax-form', function(event){
    var $this = $(this)
    var action_container = $this.parents('.action-interation-container').first()
    var interaction_type = action_container.data('interaction_kind')
    var formid = $this.attr('id');
    var button = $this.find('button.active[type="submit"]').last();
    if(button.val() == 'Cancel'){
      hide_action_interaction_container(action_container)
      event.preventDefault();
      return
    }
    var url = $(event.target).attr('action');
    $(button).addClass('disabled');
    var formData = new FormData($(this)[0]);
    formData.append(button.val(), button.val())
    var action = $('#'+action_container.data('action_id'))
    var action_metadata = get_action_metadata(action)
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
          }
          catch(err) {};
         finish_progress()
        }else if(! (data.redirect_url && !data.ignore_redirect)){
          hide_action_interaction_container(action_container)
          finish_progress()
        }
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


$(document).on('click', '.sidebar-nav-items .item-activator.desabled', function(event){
      var $this = $(this)
      $this.removeClass('desabled')
      $this.parents('.sidebar-nav-items').first().removeClass('desabled')
});

$(document).on('click', '.sidebar-nav-items .item-activator:not(.desabled)', function(event){
      var $this = $(this)
      $this.addClass('desabled')
      $this.parents('.sidebar-nav-items').first().addClass('desabled')
});

$(document).on('click', function(event){
      var $this = $(this)
      var parents = $($(event.target).parents('.sidebar-nav-items:not(.desabled)'))
      if(parents.length == 0){
         $('.sidebar-nav-items').addClass('desabled');
         $('.sidebar-nav-items .item-activator').addClass('desabled')
      }
});

$(document).on('click', '.sidebar-nav-items .item.closed',function(event){
      var $this = $(this)
      var to_open = $('#'+$this.data('target'))
      open_sidebar_container_item(to_open)
});

$(document).on('resources_loaded', function(){
  load_views()
})