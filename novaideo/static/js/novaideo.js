function switchon(slide_toggle){
    if ($('#navbaruser').hasClass('hide-bloc')){
       if (slide_toggle){$('#navbaruser').slideToggle("fast");}
       $('#navbaruser').removeClass('hide-bloc');
       $('.novaideo-content').css('margin-top', '0px')
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
       $('.novaideo-content').css('margin-top', '20px')
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
          //$('.switchchoice').click();
      };
      switchoff(!is_init);
    }
};


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
        item.height(element.height()+9)
     }
};

function init_seemore(){
  $('.seemore').on('click', function(){
      var item = $(this).parents('#item-datas').first();
      var child = $(item).find('.more-item.hide-bloc').first();
      $(child).removeClass('hide-bloc');
      child = $(item).find('.more-item.hide-bloc');
      if (child.length == 0) {$(this).addClass('hide-bloc')} 
   });

};

function init_content_text(){
     var texts = $('.content-text');
     for(i=0; i<texts.length; i++){
         if ($(texts[i]).height()>600){
             $(texts[i]).addClass("content-text-scroll")
         }
     }
};


$(document).ready(function(){

  $( window ).resize(function(){
    resize_search_result()
  });

  $("[name='globalmenuswitch']").bootstrapSwitch();

  init_switch();
  init_content_text();
  /*$($('.alert.alert-danger').parents('.panel.panel-default').first()).on('shown.bs.collapse', function () {
      if ($(this).find('pan'))
      resize_search_result()
  });
*/

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

  init_seemore();
  
  initscroll();
});

