function init_admin_nav(){
   var adminnav = $('#adminnavbar');
   var actions = $(adminnav.find('ul').first());
   if (!actions.hasClass('hide-bloc')){
     var menueheight = actions.height()+5;
     adminnav.css({'height': menueheight+'px'});
   }else{
     adminnav.css({'height': '180px'});
   }
}


function admin_nav_on(event, element){
        var parent = $($(element).parents('#adminnavbar').first());
        var target = parent.find('.admin-nav');
        $.cookie('admin_nav', 'on', {path: '/',  expires: 1});
        $(element).animate({left: '+='+187}, 500);
        $(element).removeClass('admin-off');
        $(element).addClass('admin-on');
        $(element).find('.admin-nav-label').addClass('hide-bloc');
        $(target).removeClass('hide-bloc');
        var adminnav = $('#adminnavbar');
        var menueheight = $(adminnav.find('ul').first()).height()+5;
        adminnav.css({'height': menueheight+'px'});
        //$(target).show(300);
};

function admin_nav_off(event, element){
        var parent = $($(element).parents('#adminnavbar').first());
        var target = parent.find('.admin-nav');
        $.cookie('admin_nav', 'off', {path: '/',  expires: 1});
        //target.hide(300);
        $(element).animate({left: '-='+187}, 500);
        $(element).addClass('admin-off');
        $(element).removeClass('admin-on');
        $(element).find('.admin-nav-label').removeClass('hide-bloc');
        setTimeout(function() {
           $(target).addClass('hide-bloc');
           var adminnav = $('#adminnavbar');
           adminnav.css({'height': '180px'});
        }, 510);
        
};

function admin_nav_onclick(event){
  if ($(event.target).hasClass('admin-call') || $(event.target).hasClass('admin-nav-title')){
    if ($(this).hasClass( "admin-on" )){
      admin_nav_off(event, this)
    }else{
      admin_nav_on(event, this)
    }
   }
};


function activate_explanation(event){
  if(!$(event.target).hasClass('close')){
    var explanation = $($(this).find('.proposal-explanation').first());
    explanation.removeClass('hide-bloc');}
};

function close_explanation(event){
    var explanation = $($(this).parents('.proposal-explanation').first());
    explanation.addClass('hide-bloc');
};

function switchon(slide_toggle){
    if ($('#navbaruser').hasClass('hide-bloc')){
       if (slide_toggle){$('#navbaruser').slideToggle("fast");}
       $('#navbaruser').removeClass('hide-bloc');
       var steps_container = $('.steps-container.row');
       var novaideo_contents = $('.novaideo-contents');
       if (novaideo_contents.length > 0){
           novaideo_contents.css('margin-top', '-20px')
       }else{
          if (steps_container.length > 0){
           steps_container.css('margin-top', '0px')
          }else{
            $('.novaideo-content').css('margin-top', '0px')
          }
        }
    };
    if (!$('#searchform').hasClass('hide-bloc')){
       if (slide_toggle){$('#searchform').slideToggle("fast");}
       $('#searchform').addClass('hide-bloc');
    };
};


function switchoff(slide_toggle){
    if (!$('#navbaruser').hasClass('hide-bloc')){
       if (slide_toggle){$('#navbaruser').slideToggle("fast");}
       $('#navbaruser').addClass('hide-bloc');
       var steps_container = $('.steps-container.row');
       var novaideo_contents = $('.novaideo-contents');
       if (novaideo_contents.length > 0){
           novaideo_contents.css('margin-top', '10px')
       }else{
          if (steps_container.length > 0){
           steps_container.css('margin-top', '20px')
          }else{
            $('.novaideo-content').css('margin-top', '20px')
          }
        }
    };
    if ($('#searchform').hasClass('hide-bloc')){
       if (slide_toggle){$('#searchform').slideToggle("fast");}
       $('#searchform').removeClass('hide-bloc');
    };
};


function menuSwitchChange(state, is_init) {
    $.cookie('menu_switch_state', state, {path: '/',  expires: 1});
    if (state==true){
      if (is_init){
          $('input[name="globalmenuswitch"]').bootstrapSwitch('state', true);
          //$('.switchchoice').click();
      };
      switchon(!is_init);
    }else{
      if (is_init){
          $('input[name="globalmenuswitch"]').bootstrapSwitch('state', false);
      };
      switchoff(!is_init);
    }
};

function set_visited(){
    $.cookie('visited', 'true', {path: '/',  expires: 1});
}

function init_switch() {
    var menustate = $.cookie('menu_switch_state');
    if(menustate) {
      state = false;
      if (menustate=='true'){state = true;};
      menuSwitchChange(state, true)
    }else{
      menuSwitchChange(true, true);
    };
    init_switch = function(){};
};

function initscroll(){
  $('.results').infinitescroll({
    navSelector  : ".results .batch",
                   // selector for the paged navigation (it will be hidden)
    nextSelector : ".results .pager .next",
                   // selector for the NEXT link (to page 2)
    itemSelector : ".results div.col-md-12",
                   // selector for all items you'll retrieve
    pathParse: function(path, next_page) {
       var parts = path.match(/^(.*?batch_num=)1(.*|$)/).slice(1);
// ["http://0.0.0.0:6543/@@seemyideas?batch_num=", "&batch_size=1&action_uid=-4657697968224339750"]
// substanced Batch starts at 0, not 1
       var f = function(currPage) {
         return parts.join(currPage - 1);
       };
       return f;
    },
    loading: {
      finishedMsg: "<em>No more item.</em>"
    }
  });

};

function resize_search_result(){
     var results = $('.search-item'); 
     for (d=0; d< results.length; d++){
        var element = $(results[d]);
        var item = element.children().filter('.content-image')
        item.height(element.height()+8)
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

function init_result_scroll(){
  var last_child = $('.result-scroll .search-item:last-child');
  if (last_child.length > 0){
      var top = last_child.offset().top - $('.result-scroll').offset().top  + last_child.height() + 30
      if (top < 1600){
       $('.result-scroll').height(top)
      }
  }else{
       $('.result-scroll').height(100)
  }
};

$(document).ready(function(){

  set_visited();
  
  $( window ).resize(function(){
    resize_search_result()
  });

  $("[name='globalmenuswitch']").bootstrapSwitch();

  init_switch();

  init_content_text();

  init_result_scroll();

  init_admin_nav();

  $('.admin-call').on('click', admin_nav_onclick);

  $('.proposal-opinion').on('click', activate_explanation);

  $('.proposal-opinion button.close').on('click', close_explanation);

  $('.control-form-button').on('click', function(){
        var form = $($(this).parents('div.ajax-form').first()).find('.controled-form').first();
        if (form.hasClass('hide-bloc')) {
            form.removeClass('hide-bloc')           
        }else{
            form.addClass('hide-bloc')       }
    });

  $('input[name="globalmenuswitch"]').unbind("switchChange.bootstrapSwitch").bind('switchChange.bootstrapSwitch',function(event, state) {
     menuSwitchChange(state, false);
  });

  $($('.search-item').parents('.panel-group').first()).find('.panel-collapse').on('shown.bs.collapse', function () {
      resize_search_result()
  });

  $('.panel-collapse.collapse .results').attr('class', 'results-collapse');

  $('.panel-collapse').on('hidden.bs.collapse', function () {
      $(this).find('.result-collapse').attr('class', 'results-collapse');
      $('.results').attr('infinitescroll', null)
  });

  $('.panel-collapse').on('shown.bs.collapse', function () {
      $(this).find('.results-collapse').attr('class', 'results');
      initscroll()
  });

  $('nav a nav-control').on('click', function(){
      $(".navbar-toggle").click();
  });

  $('.panel-collapse').on('hide.bs.collapse', function () {
    $(this).siblings().find('a span').attr('class', 'glyphicon glyphicon-plus');
  });

  $('.panel-collapse').on('show.bs.collapse', function () {
    $(this).siblings().find('a span').attr('class', 'glyphicon glyphicon-minus');
  });

  $('.scroll-able.result-scroll').endlessScroll({
      fireOnce: false,
      callback: function(i, n, p) {
        $(window).scroll()
      }
    });
  
  initscroll();
});



