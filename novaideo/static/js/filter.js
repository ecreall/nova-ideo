function open_filter(filter_container){
  filter_container.removeClass('closed')
  .addClass('open')
  filter_container.find('.filter-btn').removeClass('md-expand-more closed')
  .addClass('md-expand-less open')
  filter_container.find('.filter-form').css('display', 'block');

}

function close_filter(filter_container){
  filter_container.removeClass('open')
  .addClass('closed')
  filter_container.find('.filter-btn').removeClass('md-expand-less open')
  .addClass('md-expand-more closed')
  filter_container.find('.filter-form').css('display', 'none');
}

function init_filter_text_input(filter_container){
  var filter_input = filter_container.find('.filter-input-container input.filter-input').first()
  var form = filter_container.find('.filter-form form');
  var text_to_serach = form.find('input.form-control[name="text_to_search"]').first()
   filter_input.val(text_to_serach.val())
   filter_input.attr('value', text_to_serach.val())
}

function activate_filter(event){
  var $this = $(this)
  var filter_container = $this.parents('.filter-container')
  if($this.hasClass('closed')){
    open_filter(filter_container)
  }else{
    close_filter(filter_container)
  }
};

function filter(event){
  //if change on select2 search field then return
  if($(event.target).hasClass('select2-search__field')){
    return
  }
  var form = $(this)
  var filter_container = $(form.parents('.filter-container'));
  var is_open = filter_container.hasClass('open')
  var filter_activator = $(filter_container.find('.filter-activator').first());
  var data_get = $(form).serialize();
  data_get += '&'+'op=filter_result';
  var filter_container_id = filter_container.parents('div').first().attr('id')
  var target_title = undefined;
  if(filter_container_id){
    target_title = filter_container.parents('.content-view').first().find('#'+filter_container_id+'-title')
  }
  if(!target_title || target_title.length==0){
    target_title = $('.pontus-main .panel-heading').first();
  }
  var target = $(form.parents('.items-main-view-container'));
  var id = target.attr('id')
  var url = filter_activator.data('url');
  var filter_source = filter_activator.data('filter_source')
  if (filter_source !== ''){
    data_get += '&'+'filter_source='+filter_source;
  }
  data_get += '&'+'filter_result=true';
  var sort_form = $(target.find('.sort-container form').first());
  if(sort_form.length>0){
      data_get += '&'+sort_form.serialize();
  }
  data_get += '&load_view=load';
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
            var result_target = result_body.find('#'+id)
            var filter_container_target = result_target.find('.filter-container')
            init_filter_text_input(filter_container_target)
            if(is_open){
              open_filter(filter_container_target)
            }else{
              close_filter(filter_container_target)
            }
            source_tab.html(tab.html())
            // update view title
            var new_title =  filter_container_target.find('.filter-activator').first().data('filter_message');
            target_title.html("<div class=\"panel-title\"><h4>"+new_title+"</h4></div>");
            // update results
            target.html(result_target.html());
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
  var is_open = filter_container? filter_container.hasClass('open'): false;
  var filter_form = $(filter_container.find('form'));
  var url = sort_form.data('url')
  var data_get = ''
  if (filter_form.length > 0){
      var filter_activator = $(filter_container.find('.filter-activator').first());
      data_get = filter_form.serialize();
      data_get += '&'+'op=filter_result';
      url = filter_activator.data('url');
      var filter_source = filter_activator.data('filter_source')
      if (filter_source !== ''){
        data_get += '&'+'filter_source='+filter_source;
      }
      data_get += '&'+'filter_result=true';
      data_get += '&'+'is_sort=true';
      data_get += '&'+'view_only=1';
  }
  url = url?url: window.href
  var filter_container_id = filter_container.parents('div').first().attr('id')
  var target_title = undefined;
  if(filter_container_id){
    target_title = filter_container.parents('.content-view').first().find('#'+filter_container_id+'-title')
  }
  if(!target_title || target_title.length==0){
    target_title = $('.pontus-main .panel-heading').first();
  }
  var id = target.attr('id')
  data_get += '&'+sort_form.serialize();
  data_get += '&load_view=load';
  
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
              var result_target = result_body.find('#'+id)
              var filter_container_target = result_target.find('.filter-container')
              init_filter_text_input(filter_container_target)
              if(is_open){
                open_filter(filter_container_target)
              }else{
                close_filter(filter_container_target)
              }
              source_tab.html(tab.html())
              // update view title
              var new_title = filter_container_target.find('.filter-activator').first().data('filter_message');
              target_title.html("<div class=\"panel-title\"><h4>"+new_title+"</h4></div>");
              // update results
              target.html(result_target.html());
             try {
                  deform.processCallbacks();
              }
              catch(err) {};
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
              initscroll();
          }
        }
        finish_progress()
    });
  //}, 5000);
 

}


$(document).on('keypress', '.filter-container .filter-input-container input', function (event) {
  if (event.keyCode == 13 || event.keyCode == 10) {
    var $this = $(this)
    var form = $this.parents('.filter-container').first().find('.filter-form form');
    var text_to_serach = form.find('input.form-control[name="text_to_search"]').first()
    text_to_serach.val($this.val()).trigger('change')
  }
});

$(document).on('click', '.filter-btn', activate_filter);

$(document).on('change', '.filter-form form', filter);

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

