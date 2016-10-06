
function search_result_template(oid){ 
  return  '<span data-oid="'+oid+'" id="search_container_'+oid+'" class="live-search-container select2-container select2-container--default select2-container--open" style="position: absolute; z-index: 1200;">'
    +'<span class="select2-dropdown select2-dropdown--below" dir="ltr">'
    +'<span class="select2-search select2-search--dropdown">'
    +'<span class="select2-results">'
    +'<div role="tree" class="select2-results__options" id="select2-fd8w-results" aria-expanded="true" aria-hidden="false"></div>'
    +'</span></span></span>'
}

var search_params = {};

function init_params(oid){
  search_params[oid] = {params: {page: 1, pageLimit: 30},
                        more: true
                        }
}

function add_search_container(input){
  var oid = $(input).attr('id');
  init_params(oid);
  $('body').append(search_result_template(oid));
  var search_container = $('body #search_container_'+oid+'');
  search_container.css('display', 'none');
  $(input).unbind('keyup');
  $(input).bind('keyup', function(){
    if(search_container.css('display') == 'none'){
      var offset = $(this).offset();
      var height = $(this).height();
      var offset_nav = $('.user-nav-top').offset();
      var width = $('.user-nav-top').width();
      search_container.css('left', String(offset_nav.left)+'px');
      search_container.css('top', String(offset.top+height+14)+'px');
      $(search_container.find('.select2-dropdown')).css('width', width+'px')
      search_container.css('display', 'block');
    }
  });
  var timeout = null;
  var $input = $(input);
  $input.bind('keyup', function(){
     loading_progress();
    $(search_container.find('div.select2-results__options')).empty();
    init_params(oid);
    clearTimeout(timeout);
    timeout = setTimeout(function() { find_items($input) }, 400);
  });

  $(document).on('click', function(event){
       if($(this) != $(input)){
           search_container.css('display', 'none');
       }
    });
}

function append_results(body){
  $('.select2-container div.select2-results__options').html(body);
}


function find_items(input){
      var oid = $(input).attr('id');
      var url = $(input).data('url');
      var form = input.parents('form').first()
      var formData = form.serialize();
      
      $.getJSON(url, formData, function(data) {
            if(data){
              append_results(data['body']);
            }
           finish_progress();
        });
}

function submit_live_serach_form(element){
  var oid = $($(element).parents('.live-search-container').first()).data('oid');
  var btn = $($('#'+oid+'.search-text-input').parents('#searchsection').find('button[type="submit"]').first());
  btn.click()
}

$(document).ready(function(){
  var search_inputs = $('.search-text-input');
  for(var i=0; i<search_inputs.length; i++){
    add_search_container($(search_inputs[i]))
  }
});
