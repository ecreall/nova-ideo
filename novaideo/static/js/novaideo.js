function switchon(){
    if (!$('#navbaruser').is(':visible')){
       $('#navbaruser').slideToggle("fast");
    };
    if ($('#searchform').is(':visible')){
       $('#searchform').slideToggle("fast");
    };
};


function switchoff(){
    if ($('#navbaruser').is(':visible')){
       $('#navbaruser').slideToggle("fast");
    };
    if (!$('#searchform').is(':visible')){
       $('#searchform').slideToggle("fast");
    };
};


function menuSwitchChange(state, is_init) {
    $.cookie('menu_switch_state', state, {path: '/',  expires: 1});
    if (state==true){
      if (is_init){
          $('input[name="globalmenuswitch"]').bootstrapSwitch('state', true);
          //$('.switchchoice').click();
      };
      switchon();
    }else{
      if (is_init){
          $('input[name="globalmenuswitch"]').bootstrapSwitch('state', false);
          //$('.switchchoice').click();
      };
      switchoff();
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


$(document).ready(function(){
  $( window ).resize(function(){
    resize_search_result()
  });

  $("[name='globalmenuswitch']").bootstrapSwitch();

  init_switch();

  $('input[name="globalmenuswitch"]').unbind("switchChange.bootstrapSwitch").bind('switchChange.bootstrapSwitch',function(event, state) {
     menuSwitchChange(state, false);
  });
  $('#ideatext p').on('select',function(event){
               alert(event)
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

