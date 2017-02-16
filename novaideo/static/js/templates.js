
function related_item_template(item){
   var markup = '<div class="clearfix">' +
                '<div class="col-sm-1">'
   if(item.icon){
      markup += '<span class=\"search-icon '+item.icon+'\"></span>'
   };
   markup += '</div>'+
             '<div clas="col-sm-10">' +
               '<div class="clearfix">' +
                  '<div class="col-sm-8">' + item.text + '</div>';
   if (item.description) {
      markup += '<div class="col-sm-3">' + item.description + '</div>';
    };
   markup += '</div></div></div>';
   return markup
};


function user_item_template(item){
  var markup = '<div>';
  if(item.img_url){
      markup += '<img width="25" src=\"'+item.img_url+'\" class="author-img img-circle"> ';
  }
  markup += item.text+'</div>';
  return markup
};


try {
    select2_ajax_templates['related_item_template'] = related_item_template;
    select2_ajax_templates['user_item_template'] = user_item_template;
}
catch(err) {
}