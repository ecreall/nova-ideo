function loading_progress(){
    $('img.lac-loading-indicator').removeClass('hide-bloc');
}

function finish_progress(){
    $('img.lac-loading-indicator').addClass('hide-bloc');
}

function update_notification_id(id, url){
   $.post(url, {id: id}, function(data) {
     console.log(data)

   });
}

function send_vote(event){
  var $this = $(this)
  var panel = $($this.parents('.panel').first())
  var group = $($this.parents('.panel-group'))
  var button = $($this.find('button').first())
  var formData = new FormData($this[0]);
  formData.append(button.val(), button.val())
  var url = $this.attr('action')
  button.addClass('disabled');
  loading_progress()
  $.ajax({
      url: url,
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function(data) {
        panel.remove()
        var votes = $(group.find('.panel-title.collapsed'))
        if(votes.length>0){
          $(votes.first()).click()
          finish_progress()
        }else{
           location.reload();
        }
       }
  });
  event.preventDefault();
}

function collapse_current_collpsein(){
  var current_btn = $(this);
  var btns = $('.navbar-toggle.collapsed');
  for(var i = 0; i<= btns.length; i++){
      var btn = $(btns[i]);
      if (btn != current_btn){
        $(btn.data('target')).collapse('hide');
      }
  }

}

function activate_explanation(event){
  if($(event.target).parents('.proposal-explanation').length == 0){
    var explanation = $($(this).find('.proposal-explanation').first());
    explanation.removeClass('hide-bloc');}
};

function close_explanation(event){
    var explanation = $($(this).parents('.proposal-explanation').first());
    explanation.addClass('hide-bloc');
};


function set_visited(){
    $.cookie('visited', 'true', {path: '/',  expires: 1});
}


function reset_cookie_channels_bar(){
  var $this = $('.all-channels');
  if ($this.hasClass('toggled')){
    $.cookie('channels', 'off', {path: '/',  expires: 1});
  }else{
     $.cookie('channels', 'on', {path: '/',  expires: 1});
  }
}

function init_channels_scroll(){
$('.channels-container').mCustomScrollbar({
    theme:"minimal-dark",
    scrollInertia: 100,
  });
}

function initscroll(){
  var result_scrolls = $(".result-scroll")
  for(var i = 0; i<= result_scrolls.length; i++){
    var result_scroll = $(result_scrolls[i]);
    var id = result_scroll.attr('id')
    result_scroll.mCustomScrollbar({
    theme:"minimal-dark",
    scrollInertia: 100,
    callbacks:{
      onTotalScroll:function(){
        $(this).trigger('scroll');
      }
    }
  });
  $(result_scroll.find('.mCSB_container')).infinitescroll({
    behavior: 'local',
    bufferPx: 0,

    binder: result_scroll,
    navSelector  : "#"+id+" .batch",
                   // selector for the paged navigation (it will be hidden)
    nextSelector : "#"+id+" .pager .next",
                   // selector for the NEXT link (to page 2)
    itemSelector : "#"+id+" .result-container",

    pathParse: function(path, next_page) {
       var new_path = path;
       var id = result_scroll.attr('id')
       var filter = $('#filter-'+id);
       if (filter.length>0){
            var form = $($(filter).find('form').first());
            var filter_container = $(form.parents('.filter-container'));
            var filter_btn = $(filter_container.find('.filter-btn').first());
            var data_get = $(form).serialize();
            data_get += '&'+'op=filter_result';
            var filter_source = filter_btn.data('filter_source');
            if (filter_source !== ''){
              data_get += '&'+'filter_source='+filter_source;
            }
            data_get += '&'+'filter_result=true';
            data_get += '&'+'scroll=true';
            data_get += '&'+'view_only=1';
            new_path += '&'+ data_get;
      };
      // var parts = new_path.match(/^(.*?batch_num=)1(.*|$)/).slice(1);
// ["http://0.0.0.0:6543/@@seemyideas?batch_num=", "&batch_size=1&action_uid=-4657697968224339750"]
// substanced Batch starts at 0, not 1
       var f = function(currPage) {
          var next_path = $($('#'+id+' .result-container').first().parents('div').first().find('>.result-container').last()).data('nex_url')
          return next_path +'&'+ data_get;
       };
       return f;
    },
    loading: {
      finishedMsg: '<span class="label label-warning">'+ novaideo_translate("No more item.")+"</span>",
      img: window.location.protocol + "//" + window.location.host + "/novaideostatic/images/progress_bar.gif",
      msgText: "",
    }
  });
}
};


function init_content_text(){
     var texts = $('.content-text');
     for(i=0; i<texts.length; i++){
         if ($(texts[i]).height()>600){
             $(texts[i]).addClass("content-text-scroll")
         }
     }
};

function init_result_scroll(event, default_top, element){
  if(default_top == undefined){
    default_top = 1600
  }
  var result_scrolls = element? $(element.find('.result-scroll')): $('.result-scroll');
  for(var i = 0; i<= result_scrolls.length; i++){
    var result_scroll = $(result_scrolls[i]);
    var items = $(result_scroll.find('.result-item, .small-result'));
    var last_child = items.last()
    if (last_child.length > 0){
        var top = last_child.offset().top - result_scroll.offset().top  + last_child.height()
        if(items.length < 8){
          top += 50
        }else{
          top -= 10
        }
        if (top < default_top){
         result_scroll.height(top);
        }else{
          result_scroll.height(default_top);
        }
    }else{
         result_scroll.height(100);
    }
 }
};

function init_morecontent_scroll(){
  var result_scrolls = $('.more-content-carousel');
  for(var i = 0; i<= result_scrolls.length; i++){
    var result_scroll = $(result_scrolls[i]);
    var last_child = $(result_scroll.find('.search-item').last());
    if (last_child.length > 0){
        var top = last_child.offset().top - result_scroll.offset().top  + last_child.height() + 150
        if (top < 1600){
         result_scroll.height(top);
        }
    }else{
         result_scroll.height(100);
    }
 }
};


function more_content(elements, isvertical){
    try{
      elements.slick({
        vertical: isvertical,
        centerMode: true,
        dots: false,
        slidesToShow: 5,
        slidesToScroll: 5,
        // autoplay: true,
        // autoplaySpeed: 8000,
        // infinite: true,
        responsive: [
            {
              breakpoint: 1024,
              settings: {
                slidesToShow: 5,
                slidesToScroll: 5,
                // infinite: true,
                dots: false
              }
            },
            {
              breakpoint: 600,
              settings: {
                slidesToShow: 2,
                slidesToScroll: 2
              }
            },
            {
              breakpoint: 480,
              settings: {
                slidesToShow: 1,
                slidesToScroll: 1
              }
            }
            // You can unslick at a given breakpoint now by adding:
            // settings: "unslick"
            // instead of a settings object
         ]
       });
  }
  catch(err) {
  }

}


function scroll_to_panel(){
  var url = document.location.toString();
  if ( url.match('#') ) {
      var panel = $('#'+url.split('#')[1])
      panel.addClass('in');
      panel.animate({scrollTop : 0},800);
  }
}


function update_inline_action(url){
    var $this = $(this)
    var target = $($this.parents('.search-item, .content-view').find('.actions-footer-container').first())//closest('.dace-action-inline').data('target')+'-target';
    var actions = $($this.parents('.actions-block').find('.dace-action-inline'));
    if($this.hasClass('activated')){
       target.slideUp();
       actions.removeClass('activated')
       return
    }
    actions.removeClass('activated')
    var url = $this.closest('.dace-action-inline').data('updateurl');
    $.getJSON(url,{tomerge:'True', coordinates:'main'}, function(data) {
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
        }else{
           location.reload();
           return false
        }
    });
    return false;
};

function update_inline_sidebar_action(url){
    var $this = $(this)
    var actions = $('.dace-action-inline');
    if($this.hasClass('activated')){
       actions.removeClass('activated')
       return
    }
    var sidebar = $('.sidebar-right-nav')
    var target = $(sidebar.find('.actions-footer-container'))//closest('.dace-action-inline').data('target')+'-target';
    var toggle = $('.menu-right-toggle:not(.close)')
    var toggle = $('.menu-right-toggle:not(.close)')
    var title = $($this.parents('.view-item').first().find('.view-item-title')).clone()
    title.find('.label-basic').remove()
    actions.removeClass('activated')
    var url = $this.closest('.dace-action-inline').data('updateurl');
    loading_progress()
    $.getJSON(url,{tomerge:'True', coordinates:'main'}, function(data) {
       var action_body = data['body'];
       if (action_body){
           $(target.find('.container-body')).html(action_body);
           if(title.length > 0){
               $(sidebar.find('.sidebar-title .entity-title')).html(title)
           }
           $this.addClass('activated')
           try {
                deform.processCallbacks();
            }
           catch(err) {};
           if(toggle.length>0){
              toggle.click()
           }
           init_comment_scroll(target)
           finish_progress()
        }else{
           location.reload();
           return false
        }
    });
    return false;
};

function open_add_idea_form(){
$(".home-add-idea .form-group:not(.idea-text),"+
     ".home-add-idea .form-group label,"+
     ".home-add-idea .form-group.idea-text #desc").slideDown();
    $(".home-add-idea").addClass('opened').removeClass('closed')
}

function close_add_idea_form(){
   $(".home-add-idea .form-group:not(.idea-text),"+
     ".home-add-idea .form-group label,"+
     ".home-add-idea .form-group.idea-text #desc").slideUp();
    $(".home-add-idea").addClass('closed').removeClass('opened')
    $(".similar-ideas.modal").modal('hide')
  }

$(document).on('click', '.full-screen-btn.small', function(){
    var $this = $(this)
    $('.pontus-main').addClass('full-screen');
    $this.removeClass('glyphicon glyphicon-resize-full').addClass('glyphicon glyphicon-resize-small')
    $this.removeClass('small').addClass('full')
    $('.pontus-main').removeClass('small').addClass('full')

});

$(document).on('click', '.full-screen-btn.full', function(){
    var $this = $(this)
    $('.pontus-main').removeClass('full-screen');
    $this.removeClass('glyphicon glyphicon-resize-small').addClass('glyphicon glyphicon-resize-full')
    $this.removeClass('full').addClass('small')
    $('.pontus-main').removeClass('full').addClass('small')

});

$(document).on('click', '.proposal-opinion', activate_explanation);

$(document).on('click', '.proposal-opinion button.close', close_explanation);

$(document).on('click', '.working-group-toggle', function(){
    var $this = $(this)
      var wg_section_body = $($this.parents('.working-group-result').first().find('.working-group-section').first());
      var btn = $($this.find('.working-group-toggle-btn').first());
      
      if(wg_section_body.hasClass('hide-bloc')){
       btn.addClass('ion-ios7-arrow-up');
        btn.removeClass(' ion-ios7-arrow-down');
        wg_section_body.removeClass('hide-bloc');
      }else{
        btn.removeClass('ion-ios7-arrow-up');
        btn.addClass(' ion-ios7-arrow-down');
        wg_section_body.addClass('hide-bloc');
      };
      
      init_result_scroll();
        
  });


$(document).on('click', '.proposal-support .token:not(.disabled)', function(){
   var $this = $(this)
   var opposit_class = $this.hasClass('token-success')? '.danger': '.success';
   var supportbloc = $($this.parents('.proposal-support').first())
   var opposit = $(supportbloc.find('.label'+opposit_class).first())
   var opposit_token = $(opposit.find('.token').first())
   var parent = $($this.parents('.label').first())
   var action_url = $this.data('action')
   var mytoken = $(parent.find('.my-token').first())
   var support_nb = $(parent.find('.support-nb').first())
   var opposit_mytoken = $(opposit.find('.my-token').first())
   var opposit_support_nb = $(opposit.find('.support-nb').first())
   if(action_url){
     loading_progress()
     $.getJSON(action_url,{}, function(data) {
          finish_progress()
          if(data['state']){
             if (data.title){
                parent.attr('title', data.title)
             }
             if (data.opposit_title){
                opposit.attr('title', data.opposit_title)
             }
            if(!data.withdraw){
             supportbloc.addClass('my-support')
             mytoken.removeClass('hide-bloc')
             var new_nb = parseInt(support_nb.text()) + 1
             support_nb.text(new_nb)
             if (data.change){
               opposit_mytoken.addClass('hide-bloc')
               var opposit_new_nb = parseInt(opposit_support_nb.text()) - 1
               opposit_support_nb.text(opposit_new_nb)
               opposit_token.data('action', data.opposit_action)
             }
            }else{
              supportbloc.removeClass('my-support')
              mytoken.addClass('hide-bloc')
              var new_nb = parseInt(support_nb.text()) - 1
              support_nb.text(new_nb)
            }
            $this.data('action', data.action)
          }
          if(data.hastoken != undefined){
            if(data.hastoken){
              $('.token.disabled').removeClass('disabled').addClass('active')
            }else{
              $('.proposal-support:not(.my-support) .token.active').removeClass('active').addClass('disabled')
            }
          }
        });
   }

})

$(document).on('click', '.sidebar-nav li > a.primary', function(event){
    var $this = $(this)
    if(!event.internal){
      $this.addClass('current')
      var menuevent = jQuery.Event( "click" );
      menuevent.internal = true;
      $('.sidebar-nav li > a.primary.active-item:not(.current)').trigger(menuevent);
      $this.removeClass('current')
    }
    var iconstate = $($this.find('span.icon-state'));
    if(iconstate.hasClass('ion-chevron-down')){
       iconstate.addClass('ion-chevron-up')
       .removeClass('ion-chevron-down')
    }else{
      iconstate.addClass('ion-chevron-down')
       .removeClass('ion-chevron-up')
    }
    if($this.hasClass('active-item')){
       $this.removeClass('active-item')
    }else{
      $this.addClass('active-item')
    }
    
})

$(document).on('click', '.sidebar-background.toggled', function(){
  $(".menu-toggle.close").click()
  $($(this).find(".comment-form-group.active")).removeClass('active')
})

$(document).on('click', '.sidebar-right-background.toggled', function(){
  $(".menu-right-toggle.close").click()
  $('.dace-action-inline.activated').click()
  $('body').removeClass('modal-open')

})

$(document).mouseup(function (e)
{
    var container = $(".home-add-idea, .select2-results");

    if (!container.is(e.target) // if the target of the click isn't the container...
        && container.has(e.target).length === 0
        && $(e.target).parents('body').length != 0) // ... nor a descendant of the container
    {
        if(!$(".home-add-idea .form-group.idea-text textarea").val()){
           close_add_idea_form()
        }
    }
});

// $(document).on('click', '.search-item-footer .dace-action-inline', update_inline_sidebar_action);

// $(document).on('click', '.content-footer .dace-action-inline', update_inline_sidebar_action);

$(document).on('click', '.dace-action-inline', update_inline_sidebar_action);

$(document).on('shown.bs.modal', '.modal', function () {
    init_result_scroll(undefined, 1000, $(this));
  });

$(document).ready(function(){
  $('.home-add-idea.closed > span.icon-idea').on('click', function(){
      $(this).siblings('form').find('.idea-text textarea').click().focus();
  })
  
  $('.hidden-js').css('display', 'none');

  $(document).on('click','.home-add-idea form .btn', function( event ) {
    $(this).addClass('active')
  })

  $(document).on('change','.home-add-idea form input[name="title"], .home-add-idea form select[name="keywords"]', function( event ) {
        var $this = $(this)
        var form = $($this.parents('form').first())
        var title = form.find('input[name="title"]').val();
        var keywords = $(form.find('select[name="keywords"]')).val();
        if ((!title || title == '') && (!keywords || keywords.length == 0)){
          event.preventDefault();
          return
        }
        var parent = $(form.parents('.home-add-idea').first());
        var target = $(parent.find('.similar-ideas'));
        var url = parent.data('url_search')
        $.getJSON(url,{title: title, keywords: keywords}, function(data) {
              if(data.body){
                $(target.find('.similar-ideas-container').first()).html(data.body)
                target.modal('show')
              }else{
                target.modal('hide')
              }
        });
       event.preventDefault();
   });

  $(document).on('submit','form.vote-form', send_vote)
  
  $(document).on('submit','.home-add-idea form', function( event ) {
        var $this = $(this)
        var button = $($this.find('button.active').first())
        if(button.val() == 'Cancel'){
          $this.find('textarea[name="text"]').val('');
          $this.find('.deform-close-button').click()
          $(button).removeClass('active');
          close_add_idea_form()
          event.preventDefault();
           return
        }
        var parent = $($this.parents('.home-add-idea').first());
        var danger_messages_container = $(parent.find('#messagedanger'));
        var title = $this.find('input[name="title"]').val();
        if (title=='')
        {
           danger_messages_container.text( novaideo_translate("The title is required!") ).show().fadeOut( 6000 );
           event.preventDefault();
           return
        }
        var text = $this.find('textarea[name="text"]').val();
        if (text=='')
        {
           danger_messages_container.text( novaideo_translate("The abstract is required!") ).show().fadeOut( 6000 );
           event.preventDefault();
           return
        }

        var keywords = $($this.find('select[name="keywords"]')).val();
        if (!keywords || keywords.length == 0)
        {
           danger_messages_container.text( novaideo_translate("Keywords are required!")).show().fadeOut( 6000 );
           event.preventDefault();
           return
        }

        var formData = new FormData($(this)[0]);
        formData.append(button.val(), button.val())
        var url = parent.data('url')
        
        // var inputs = $($(event.target).children().filter('fieldset')[0]).find('input[type|="radio"]');
        // if (version !=''){
          // progress.show();// TODO
          var buttons = $($this.find('button'))
        $(buttons).addClass('disabled');
        loading_progress()
        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
              if(data.state){
                $(data.body).hide().prependTo($('.result-container')).fadeIn(1500)
                $this.find('input[name="title"]').val(data['new_title']);
                $this.find('textarea[name="text"]').val('');
                $this.find('.deform-close-button').click()
                $(buttons).removeClass('disabled');
                $(button).removeClass('active');
                close_add_idea_form()
                finish_progress()
              }
             }
        });


       event.preventDefault();
   });

  $(".home-add-idea.closed .form-group.idea-text").click(function(e) {
      open_add_idea_form()
  });

  $(".menu-toggle").click(function(e) {
        e.preventDefault();
        $(".bar-wrapper").toggleClass("toggled");
        $('.sidebar-background').toggleClass("toggled");
    });

  $(".all-channels-toggle").click(function(e) {
        e.preventDefault();
        $(".all-channels").toggleClass("toggled");
        reset_cookie_channels_bar()
    });

   $(".menu-right-toggle").click(function(e) {
        e.preventDefault();
        var bar = $(".bar-right-wrapper")
        var open = bar.hasClass('toggled')
        bar.toggleClass("toggled");
        $('.sidebar-right-background').toggleClass("toggled");
        $('body').toggleClass('modal-open')
        if(!open){
          $('.dace-action-inline.activated').click()
          $(bar.find(".comment-form-group.active")).removeClass('active')

        }
    });


  $(".malihu-scroll").mCustomScrollbar({
    theme:"minimal-dark",
    scrollInertia: 200
  });

  $(".navbar-toggle.collapsed").on('click', collapse_current_collpsein);

  $('input, textarea').placeholder();

  set_visited();

  init_content_text();

  init_result_scroll();

  init_morecontent_scroll();

  initscroll();

  init_channels_scroll();


  $('nav a nav-control').on('click', function(){
      $(".navbar-toggle").click();
  });

  $('.panel-collapse').on('hide.bs.collapse', function () {
    $(this).siblings().find('a span').attr('class', 'glyphicon glyphicon-plus');
  });

  $('.panel-collapse').on('show.bs.collapse', function () {
    $(this).siblings().find('a span').attr('class', 'glyphicon glyphicon-minus');
  });

  $('.panel-collapse').on('shown.bs.collapse', function () {
    init_result_scroll(undefined, 1000, $(this));
  });

  // $('.scroll-able.result-scroll').endlessScroll({
  //     fireOnce: false,
  //     callback: function(i, n, p) {
  //       $(window).scroll()
  //     }
  //   });

//code adapted from http://bootsnipp.com/snippets/featured/jquery-checkbox-buttons
$(function () {
    $('.search-choices .checkbox-inline').each(function () {

        // Settings
        var $widget = $(this),
            $checkbox = $widget.find('input:checkbox'),
            $button = $('#search-choice-'+$checkbox.attr('value')),
            color = $button.data('color'),
            settings = {
                on: {
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
                }
            };

        // Event Handlers
        $button.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });

        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $button.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $button.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$button.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $button
                    .addClass('active');
                $('#'+$button.attr('id')+'-icon').removeClass('hide-bloc')
            }
            else {
                $button
                    .removeClass('active')
                $('#'+$button.attr('id')+'-icon').addClass('hide-bloc')
            }
        }

        // Initialization
        function init() {

            updateDisplay();

            // Inject the icon if applicable
            if ($button.find('.state-icon').length == 0) {
                $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i> ');
            }
        }
        init();
    });
});

  // more_content($('.more-content-carousel.verticla'), true);
  // more_content($('.more-content-carousel:not(.vertical)'), false);

  $('.alert-block:not(.off)').hover(function(){
        var $this = $(this);
        var url = $this.data('url');
        var alert_content = $($this.find('.alerts-content').first());
        var target = $(alert_content.find('.content').first());
        alert_content.find('.loading-indicator').removeClass('hide-bloc')
        alert_content.removeClass('hide-bloc');
        $.getJSON(url,{}, function(data) {
          if(data['body']){
            target.html(data['body']);
            alert_content.find('.loading-indicator').addClass('hide-bloc')
          }
        });

    }, function(){
        var $this = $(this);
        $this.find('.alerts-content').addClass('hide-bloc')
    });

  scroll_to_panel()

  $('.nav-tabs').on('shown.bs.tab', init_result_scroll)

  $(document).on('show.bs.modal', '.similar-ideas', function(){
      $('body').addClass('similar-ideas-modal-open')
  })
  $(document).on('hidden.bs.modal', '.similar-ideas', function(){
      $('body').removeClass('similar-ideas-modal-open')
  })
});
