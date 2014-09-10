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

function correct_handler(event){
    var correction = $($(this).parents('#correction').first());
    var vote = Boolean($(this).data('favour'));
    var correction_item = parseInt(correction.data('item'));
    var correction_id = parseInt(correction.data('correction'));
    var target = $($(this).parents('#proposaltext').first());
    var url = $(this).data('url');
    dict_post = {};
    dict_post['vote'] = vote;
    dict_post['item'] = correction_item;
    dict_post['correction_id'] = correction_id;
    $.get(url, dict_post, function(data) {
      //recuperer le text et le remplacer
      if (data){
        var content = $(data['body']).find('#correction_text');
        if (content){
             $(target).html($(content).html());
             $(target).find('.correction-action').on('click', correct_handler)
        }else{
           location.reload();
           return false
         };
      }else{
           location.reload();
           return false
         };
      });
    
   }

$(document).ready(function(){

  $('.correction-action').on('click', correct_handler);

  $('button.toconfirm').on('click',function(event){
       //   var form = $($(this).parents('form').first());
       //   var buttons = form.find('.form-group').last();
       //   var confirmation = form.find('#confirmation');
       //   $(buttons).hide();
       //   $(confirmation).show();

         var form = $($(this).parents('form').first());
         var confirmation = form.find('.modal.fade');
         $(confirmation).modal('show');

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

    $(document).on('submit','.compareform', function( event ) {
        var button = $(this).find('button')

        var parent = $($(this).parents('.panel-body').first());
        var target = parent.find('.compare-result');
        var progress = parent.find('#progress');
        //POST dict
        var dict_post = {};
        var inputs = $($(event.target).children().filter('fieldset')[0]).find('input[type|="radio"]');
        var version = '';
        for (i=0; i<inputs.length; i++ ){
           if (inputs[i].checked){version = $(inputs[i]).val()};
        };
        dict_post['version'] = version;
        var url = $(event.target).data('url');
        if (version !=''){
          progress.show();// TODO
          $(button).addClass('disabled');
          $.get(url, dict_post, function(data) {
                 var content = $(data).find('.compare-result');//TODO chercher le bon scrollable
                 if (content){
                     $(target).html($(content).html());
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

       };
       event.preventDefault();
   });

    $(document).on('submit','.commentform', function( event ) {
        var button = $(this).find('button')

        var intention = $(this).find('.select2-chosen').text();
        var textarea = $(this).find('textarea');
        var comment = textarea.val();

        var parent = $($(this).parents('.panel-body').first());
        var target = parent.find('.scroll-able.comments-scroll');
        var commentmessageinfo = parent.find('#commentmessageinfo');
        var commentmessageinfo = parent.find('#commentmessageinfo');
        var commentmessagesuccess = parent.find('#commentmessagesuccess');
        var commentmessagedanger = parent.find('#commentmessagedanger');
        var progress = parent.find('#progress');
        //POST dict
        var dict_post = {};
        var inputs = $($(event.target).children().filter('fieldset')[0]).children().filter('input');
        var i = 0;
        while(i<inputs.length){
           dict_post[$(inputs[i]).attr('name')] = $(inputs[i]).val();
           i++;
        };
        dict_post['comment'] = comment;
        dict_post['intention'] = intention;
        dict_post[button.val()] = '';
        var url = $(event.target).data('url');
        if (comment !='' && intention!=''){
          progress.show();// TODO
          $(button).addClass('disabled');
          $( commentmessageinfo).text( "Comment sent" ).show().fadeOut( 1000 );
          $.post(url, dict_post, function(data) {
                 var content = $(data).find('.scroll-able.comments-scroll');//TODO chercher le bon scrollable
                 if (content){
                     $(target).html($(content).html());
                     $( commentmessagesuccess).text( "Your comment is integrated" ).show().fadeOut( 3000 );
                     textarea.val('')
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

    $(document).on('submit','.respondform', function( event ) {
        var formid = $(this).attr('id');
        var button = $(this).find('button')

        var intention = $(this).find('.select2-chosen').text();
        var textarea = $(this).find('textarea');
        var comment = textarea.val();

        var parent = $($(this).parents('.panel-body').get(1));
        var modal = $(parent).find('.modal.fade:has(form[id|=\''+formid+'\'])');
        var parentform = parent.find('.commentform');
        var urlparent = $(parentform).data('url');

        var target = parent.find('.scroll-able.comments-scroll');
        var commentmessageinfo = parent.find('#commentmessageinfo');
        var commentmessageinfo = parent.find('#commentmessageinfo');
        var commentmessagesuccess = parent.find('#commentmessagesuccess');
        var commentmessagedanger = parent.find('#commentmessagedanger');
        var progress = parent.find('#progress');
        //POST dict
        var dict_post = {};
        var inputs = $($(event.target).children().filter('fieldset')[0]).children().filter('input');
        var i = 0;
        while(i<inputs.length){
           dict_post[$(inputs[i]).attr('name')] = $(inputs[i]).val();
           i++;
        };
        dict_post['comment'] = comment;
        dict_post['intention'] = intention;
        dict_post[button.val()] = '';

        var url = $(event.target).data('url');
        if (comment !='' && intention!=''){
          progress.show();// TODO
          $(modal).modal('hide');
          $( commentmessageinfo).text( "Comment sent" ).show().fadeOut( 1000 );
          $.post(url, dict_post, function(data) {
                 $( commentmessagesuccess).text( "Your comment is integrated" ).show().fadeOut( 3000 );
                 //find comments scroll div
                 $.post(urlparent, {}, function(data) {
                      var content = $(data).find('.scroll-able.comments-scroll');//TODO chercher le bon scrollable
                      if (content){
                         $(target).html($(content).html());
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

  initscroll();
});




if(!window.Kolich){
  Kolich = {};
}

Kolich.Selector = {};
Kolich.Selector.getSelected = function(){
  var t = '';
  if(window.getSelection){
    t = window.getSelection();
  }else if(document.getSelection){
    t = document.getSelection();
  }else if(document.selection){
    t = document.selection.createRange().text;
  }
  return t;
}

Kolich.Selector.mouseup = function(){
  var st = Kolich.Selector.getSelected();
  if(st!=''){
    alert("You selected:\n"+st);
  }
}

$(document).ready(function(){
  $(document).bind("mouseup", Kolich.Selector.mouseup);
});

