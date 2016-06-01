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
  var target = $($('.pontus-main .panel-body').first());
  var target_title = $($('.pontus-main .panel-heading').first());
  var url = filter_btn.data('url');
  var filter_source = filter_btn.data('filter_source')
  if (filter_source !== ''){
    data_get += '&'+'filter_source='+filter_source;
  }
  data_get += '&'+'filter_result=true';
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
            var new_title =  $($('<div>'+data['body']+'</div>').find('.filter-btn').first()).data('filter_message');
            target_title.html("<div class=\"panel-title\">"+new_title+"</div>");
            target.html(data['body']);
           try {
                deform.processCallbacks();
            }
            catch(err) {};
            initscroll();
            init_search_results()
        }
        finish_progress()
    });
  //}, 5000);
 

}

function init_filter(){
  $('.filter-btn').on('click', activate_filter);
  $('.filter-form  .form-control').on('change', filter)  
}
