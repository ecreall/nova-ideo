

function user_item_template(item){
  var markup = '<div>';
  if(item.img_url){
      markup += '<img width="25" src=\"'+item.img_url+'\" class="author-img img-circle"> ';
  }
  markup += item.text+'</div>';
  return markup
};


try {
    select2_ajax_templates['user_item_template'] = user_item_template;
}
catch(err) {
}