
function active_on(event, element){
        var parent = $($(element).parents('.select-search').first());
        var target = parent.find('.select-search-input');
        $(target).show(700);
        $(element).removeClass('search_disabled');
        $(element).addClass('search_active');
};

function disabled_on(event, element){
        var parent = $($(element).parents('.select-search').first());
        var target = parent.find('.select-search-input');
        target.hide();
        $(element).removeClass('search_active');
        $(element).addClass('search_disabled');

};

function onclick(event){
    if ($(this).hasClass( "search_active" )){
      disabled_on(event, this)
    }else{
       active_on(event, this)
    }

};

$(document).ready(function(){
  $('.select-search-input').hide();
  $('span.select-search-call').on('click',onclick);

  $('.select-search button').on('click',function(event){
        var button = $(this);
        var select_parent = $(button.parents('.select-search-input').first());
        var parent = $(button.parents('form').first());
        var target = parent.find('#'+button.data('target'));
        var dict_post = {};
        var text = $($(button.parents('.input-group').first()).children().filter('input[type|="text"]')).val();
        dict_post['text'] = text;
        var url = button.data('url');
        $(button).addClass('disabled');
        $.get(url, dict_post, function(data) {
            if (data && data.constructor == Object ){
                $(target).empty();
                for(var d in data){
                   $(target).append('<option class="newselection" value="'+d+'">'+data[d]+'</option>')
                }
            };
             $(button).removeClass('disabled');
             //disabled_on(event, select_parent);
             $(target).select2("open")
         });

     });

});

