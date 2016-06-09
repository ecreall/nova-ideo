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
            var new_title =  $(result_body.find('.filter-btn').first()).data('filter_message');
            target_title.html("<div class=\"panel-title\"><h4>"+new_title+"</h4></div>");

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


$(document).on('click', '.filter-btn', activate_filter);

$(document).on('change', '.filter-form  .form-control', filter);