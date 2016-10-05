function activate_filter(event){
  var filter_form = $($(this).parents('.filter-container').find('.filter-form').first());
  if($(this).hasClass('closed')){
    filter_form.slideDown( );
    filter_form.removeClass('hide-bloc');
    $(this).removeClass('closed');
    $(this).addClass('open');
  }else{
    filter_form.slideUp( );
    filter_form.addClass('hide-bloc');
    $(this).removeClass('open');
    $(this).addClass('closed');
  }
};

function filter(){
  var form = $($(this).parents('form').first());
  var filter_container = $(form.parents('.filter-container'));
  var filter_btn = $(filter_container.find('.filter-btn').first());
  var data_get = $(form).serialize();
  data_get += '&'+'op=filter_result';
  // var target = $($('.pontus-main .panel-body').first());
  var target_title = $($('.pontus-main .panel-heading').first());
  var target = $(form.parents('.items-main-view-container'));
  var id = target.attr('id')
  var url = filter_btn.data('url');
  var filter_source = filter_btn.data('filter_source')
  if (filter_source !== ''){
    data_get += '&'+'filter_source='+filter_source;
  }
  data_get += '&'+'filter_result=true';
  var sort_form = $(target.find('.sort-container form').first());
  if(sort_form.length>0){
      data_get += '&'+sort_form.serialize();
  }
  loading_progress()
  //window.setTimeout(function(){
  $.post(url,data_get, function(data) {
        var selects = $(form.find('select'));
        for(var i=0; i<selects.length; i++){
          var select = $(selects[i]);
          try {
              select.select2("close");
            }
          catch(err) {};
        }
        if(data['body']){
            var result_body = $('<div>'+data['body']+'</div>')
            var source_tab_id = $(target.parents('.tab-pane').first()).attr('id')
            // update tab title
            var source_tab = $('.pontus-main ul.nav.nav-tabs > li > a[href="#'+source_tab_id+'"]')
            var tab = result_body.find('ul.nav.nav-tabs > li > a[href="#'+source_tab_id+'"]').first()
            source_tab.html(tab.html())
            // update view title
            var new_title =  $(result_body.find('.filter-btn').first()).data('filter_message');
            target_title.html("<div class=\"panel-title\"><h4>"+new_title+"</h4></div>");
            // update results
            target.html(result_body.find('#'+id).html());
           try {
                deform.processCallbacks();
            }
            catch(err) {};
            initscroll();
        }
        finish_progress()
    });
  //}, 5000);
 

}


function sort(){
  var sort_form = $(this)
  var target = $(sort_form.parents('.items-main-view-container').first());
  var filter_container = $(target.find('.filter-container'));
  var filter_form = $(filter_container.find('form'));
  var url = window.href
  var data_get = ''
  if (filter_form.length > 0){
      var filter_btn = $(filter_container.find('.filter-btn').first());
      data_get = filter_form.serialize();
      data_get += '&'+'op=filter_result';
      url = filter_btn.data('url');
      var filter_source = filter_btn.data('filter_source')
      if (filter_source !== ''){
        data_get += '&'+'filter_source='+filter_source;
      }
      data_get += '&'+'filter_result=true';
      data_get += '&'+'is_sort=true';
      data_get += '&'+'view_only=1';
  }
  // var target = $($('.pontus-main .panel-body').first());
  var target_title = $($('.pontus-main .panel-heading').first());
  var id = target.attr('id')
  data_get += '&'+sort_form.serialize();
  loading_progress()
  //window.setTimeout(function(){
  $.post(url,data_get, function(data) {
        if(filter_form.length > 0){
          var selects = $(filter_form.find('select'));
          for(var i=0; i<selects.length; i++){
            var select = $(selects[i]);
            try {
                select.select2("close");
              }
            catch(err) {};
          }
          if(data['body']){
              var result_body = $('<div>'+data['body']+'</div>')
              var source_tab_id = $(target.parents('.tab-pane').first()).attr('id')
              // update tab title
              var source_tab = $('.pontus-main ul.nav.nav-tabs > li > a[href="#'+source_tab_id+'"]')
              var tab = result_body.find('ul.nav.nav-tabs > li > a[href="#'+source_tab_id+'"]').first()
              source_tab.html(tab.html())
              // update view title
              var new_title =  $(result_body.find('.filter-btn').first()).data('filter_message');
              target_title.html("<div class=\"panel-title\"><h4>"+new_title+"</h4></div>");
              // update results
              target.html(result_body.find('#'+id).html());
             try {
                  deform.processCallbacks();
              }
              catch(err) {};
              init_result_scroll();
              initscroll();
          }

        }else{
          if (data){
              var result_body = $(data)
              target.html(result_body.find('#'+id).html());
             try {
                  deform.processCallbacks();
              }
              catch(err) {};
              init_result_scroll();
              initscroll();
          }
        }
        finish_progress()
    });
  //}, 5000);
 

}

$(document).on('click', '.filter-btn', activate_filter);

$(document).on('change', '.filter-form  .form-control', filter);

$(document).on('change', '.sort-container .sort-form', sort);

$(document).on('click', '.sort-container .sort-form .reverse-icon', function(){
  var $this = $(this)
  var input = $this.next()
  input.val('')
  if(!$this.hasClass('on')){
   input.val('on')
  }
  $this.toggleClass('on')
  input.change()
  $this.rotate({
      angle:0,
      animateTo:360
  });

});

