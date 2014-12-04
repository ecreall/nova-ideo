
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


function init_select_search(select){

  
  $($(select).find('.select-search-input').first()).hide();
  $($(select).find('span.select-search-call').first()).on('click',onclick);

  $(select+' button').on('click',function(event){
        var button = $(this);
        var select_parent = $(button.parents('.select-search-input').first());
        var parent = $(button.parents('form').first());
        var target = parent.find('#'+button.data('target'));
        var ismultiple = $(target).attr('multiple') == 'multiple';
        var dict_post = {};
        var text = $($(button.parents('.input-group').first()).children().filter('input[type|="text"]')).val();
        dict_post['text_to_search'] = text;
        var url = button.data('url');
        $(button).addClass('disabled');
        $.get(url, dict_post, function(data) {
            if (data && data.constructor == Object ){
                //$(target).empty();
                for(var d in data){
                   if ($(target).find('option[value=\"'+d+'\"]').length == 0 && !(ismultiple && d==""))
                   {
                       $(target).append('<option class="newselection" value="'+d+'">'+data[d]+'</option>')
                   }
                }
            };
             $(button).removeClass('disabled');
             //disabled_on(event, select_parent);
             $(target).select2("open")
         });

     });
}

$(document).ready(function(){

});

