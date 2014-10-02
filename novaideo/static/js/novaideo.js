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

function init_seemore(){
  $('.seemore').on('click', function(){
      var item = $(this).parents('#item-datas').first();
      var child = $(item).find('.more-item.hide-bloc').first();
      $(child).removeClass('hide-bloc');
      child = $(item).find('.more-item.hide-bloc');
      if (child.length == 0) {$(this).addClass('hide-bloc')} 
   });

};


function init_select(){
  $('.explanation-intention').on('change', function(e){
       var intention_bloc = e.val;
       var intention_form = $($($(this).parents('form').first()).find('.'+intention_bloc+'-intention').first());
       var intention_forms = $($($(this).parents('form').first()).find('.form-intention'));
       intention_forms.addClass('hide-bloc')
       if (intention_form.hasClass('hide-bloc')){
           intention_form.removeClass('hide-bloc')
       }
   });
}

function get_explanation_form(url){
              var target = $(this).data('target')+'explanation_modal';
              var url = $(this).data('url');
              $.getJSON(url,{}, function(data) {
                 var action_body = data['body'];
                 if (action_body){
                     $($(target).find('.modal-body')).html(action_body);
                     $(target).modal('show');
                     init_select();
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

function submit_explanation(url){
       var target = $($(this).parents('.modal.fade').first());
       var selectintention = $(target.find('.explanation-intention').first());
       var intention_bloc = selectintention.select2('val');
       var form = $(selectintention.parents('form').first());
       var intention_form = $(form.find('.'+intention_bloc+'-intention').first());
       var url = $(this).data('url');
       var item = $(this).data('item');

       var comment = $(intention_form.find("textarea[name='comment']").first()).val();
       var ideas = $(intention_form.find("select[name='ideas']").first()).select2('val');
       var replacedideas = $(intention_form.find("select[name='replacedideas']").first()).select2('val');
       var ideasofreplacement = $(intention_form.find("select[name='ideasofreplacement']").first()).select2('val');
       var relatedexplanation = $(form.find("select[name='relatedexplanation']").first()).select2('val');
       var intention = $(form.find("select[name='intention']").first()).select2('val');
       var datas = {'comment': comment,
                   'ideas' : ideas==undefined  || [],
                   'replacedideas': replacedideas==undefined  || [],
                   'ideasofreplacement': ideasofreplacement==undefined  || [],
                   'relatedexplanation': relatedexplanation==undefined  || [],
                   'intention': intention,
                   'item':item
                  };
       $.getJSON(url,datas, function(data) {
             $(target).modal('hide');
       });
       return false;
};

$(document).ready(function(){

  $( window ).resize(function(){
    resize_search_result()
  });

  init_select();

  $(document).on('click', '.explanation-action', get_explanation_form);
  $('.explanation-validation').on('click', submit_explanation);

  $("[name='globalmenuswitch']").bootstrapSwitch();

  init_switch();

  /*$($('.alert.alert-danger').parents('.panel.panel-default').first()).on('shown.bs.collapse', function () {
      if ($(this).find('pan'))
      resize_search_result()
  });
*/

   $('.ajax-form-button').on('click', function(){
        var form = $($(this).parents('div.ajax-form').first()).find('form').first();
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

