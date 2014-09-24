/* init items: start*/
function get_values(items){
    var values = {}
    var items = item.find('.controllable-item');
    for(i in items){
       var item = $($(items[i]).find('.actions').first())
       var oid = item.data('id');
       var title = item.data('title')
       values[oid] = title             
    };
    return values
}


function get_selecteds(select){
    var values = {}
    var selected_values = select.select2('val')
    var datas = select.select2('data')
    for(i in selected_values){
       values[i] = datas[i]             
    };
    return values
}


function init_values(){
  var related_ideas = $('div.controllable-items');
  for (c in related_ideas){
      var targetform =  $('#'+$(related_ideas[c]).data('target'));
      var target = $(targetform.find('.controlled-items'));
      var selected_values = get_selecteds(target)
      for (v in selected_values){
          $(related_ideas[c]).append(get_tag(v, selected_values[v], '', ''));
      }
      var values = get_values($(related_ideas[c]))
  }

};

/* init items: end*/


function get_tag(oid, title, body, disabled){
    return "<div class=\"panel controllable-item\">"+
        "<div class=\"panel-heading\">"+
        "<a  href=\"#panel-element-"+oid+"\" data-parent=\"#panel-controllableitems\" data-toggle=\"collapse\" class=\"panel-title\">"+
        "<span class=\"glyphicon glyphicon-plus\"> </span>  "+title+"</a>"+
        "<span class=\"actions pull-right\" data-id=\""+oid+"\">"+
        "<span title=\"Retirer de la liste\" class=\""+disabled+"del-item\"></span></span></div>"+
        "<div class=\"panel-collapse collapse\" id=\"panel-element-"+oid+"\" style=\"height: auto;\">"+
        "<div class=\"panel-body\">"+body+"</div></div></div>"
}

function init_delitem(){
  $('.del-item').on('click', function(){
      var controllable = $($(this).parents('.controllable-items').first());
      var targetform =  $('#'+controllable.data('target'));
      var target = $(targetform.find('.controlled-items'));
      var itemtodel = $($(this).parents('.actions').first()).data('id');
      var event = jQuery.Event( "delItem" );
      $(this).parents('.controllable-item').first().remove();
      event.itemid = itemtodel;
      target.trigger(event);
      last_items = controllable.find(('.controllable-item')); 
      if (last_items.length == 1){
          var last = $($(last_items[0]).find('.del-item'));
          last.removeClass('del-item');
          last.addClass('disabled-del-item');
          last.unbind("click")
      }
  });
};


$(document).ready(function(){
  init_delitem();
  $('.controlled-items').on('delItem', function(event){
        var todel = -1;
        var tab = $(this).select2('data');
        for( o in tab)
        {
          if(tab[o].id == event.itemid){todel=tab[o]}
         };
        if (todel != -1){
          tab = jQuery.grep(tab, function(value) {
             return value != todel;
          });
          $(this).select2('data', tab);
        }
  });

  $('.controlled-items').on('AddItem', function(event){
        var todel = -1;
        var tab = $(this).select2('data');
        for( o in tab)
        {
          if(tab[o].id == event.itemid){todel=tab[o]}
         };
        if (todel == -1){

            $(this).append($('<option>', {value: String(event.itemid), text: event.itemtitle}));
            var selectedItems = $(this).select2("val");
            selectedItems.push(String(event.itemid)); 
            $(this).select2("val", selectedItems);
         }
  });


   $('.new-idea-control').click(function(){
        var form = $($(this).parents('form').first());
        if (this.checked) {
            form.find('.new-idea-form').removeClass('hide-bloc');
            var search_form = $(form.find('.search-idea-form'))
            search_form.find('.select2-offscreen').select2("enable", false);
            $(search_form.find('.select-search input')).attr('disabled', true)
            $(search_form.find('.select-search button')).addClass('disabled')            
        }else{
            form.find('.new-idea-form').addClass('hide-bloc');           
            var search_form = $(form.find('.search-idea-form'))
            search_form.find('.select2-offscreen').select2("enable", true);
            $(search_form.find('.select-search input')).attr('disabled', false)
            $(search_form.find('.select-search button')).removeClass('disabled')
        }
    });



    $(document).on('click','.add-idea-form button.ajax-button', function( event ) {
        var button = $(this);
        var form = $(button.parents('form.add-idea-form').first());
        var ideas_managment = $($(form).parents('.panel-body').first());
        var related_ideas = $(ideas_managment.find('div.controllable-items'));
        var isnewidea = $(form.find('.new-idea-control'))[0].checked;
        var targetform =  $('#'+related_ideas.data('target'));
        var target = $(targetform.find('.controlled-items'));
        var danger_messages_container = $($(related_ideas.parents('div').first()).find('#messagedanger'));
        var dict_post = {};
        if (isnewidea)
         {
            newideaform = form.find('.new-idea-form');
            var title = newideaform.find('input[name="title"]').val();
            if (title=='')
            {
               danger_messages_container.text( "The title is required!" ).show().fadeOut( 6000 );
               return
            }
            var text = newideaform.find('textarea[name="description"]').val();
            if (text=='')
            {
               danger_messages_container.text( "The abstract is required!" ).show().fadeOut( 6000 );
               return
            }

            var keywords = $(newideaform.find('select[name="keywords"]')).select2('val');
            if (keywords.length == 0)
            {
               danger_messages_container.text( "Keywords are required!" ).show().fadeOut( 6000 );
               return
            }

            dict_post = {'title': title,
                         'description': text,
                         'keywords': keywords,
                         'op': 'creat_idea'};
         }else{
            oid = $($(form).find('div.search-idea-form select.select2-offscreen')).select2('val');
            var new_items = related_ideas.find('span[data-id=\"'+oid+'\"]');
            if (new_items.length>0)
            {
               danger_messages_container.text( "Idea already exist!" ).show().fadeOut( 6000 );
               return
            }
            if (oid == "")
            {
               danger_messages_container.text( "Please select a valid idea!" ).show().fadeOut( 6000 );
               return
            }
            dict_post = {'oid': oid,
                         'op': 'get_idea'};
         };
         var url = $(form).data('url');
         button.addClass('disabled');
         $.get(url, dict_post, function(data) {
             if(data){
               button.removeClass('disabled'); 
               var event = jQuery.Event( "AddItem" );
               event.itemid = data['oid'];
               event.itemtitle = data['title'];
               target.trigger(event)
               var last_items = related_ideas.find(('.controllable-item'));
               var disabled_items =  related_ideas.find(('.disabled-del-item'));
               if (disabled_items.length >0){
                   var last = $($(disabled_items[0]));
                   last.removeClass('disabled-del-item');
                   last.addClass('del-item');
                }
               var items =  related_ideas.find(('.del-item'));
               if (items.length >0){
                  related_ideas.append(get_tag(data['oid'], data['title'], data['body'], ''));
                }else{
                   related_ideas.append(get_tag(data['oid'], data['title'], data['body'], 'disabled-'));
               }
               init_seemore();
               init_delitem();
               if (isnewidea){
                  newideaform.find('input[name="title"]').val('');
                  newideaform.find('textarea[name="description"]').val('');
                  $(newideaform.find('select[name="keywords"]')).select2('val', []);
               }else{
                 $($(form).find('div.search-idea-form select.select2-offscreen')).select2('val', '')
               }
             }else{
                danger_messages_container.text( "The idea is not added!" ).show().fadeOut( 6000 );
             }
        });
   });
});
