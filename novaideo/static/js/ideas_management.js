
function get_tag(oid, title){
  return "<li class=\"list-group-item controllable-item\">" +
  "<span>"+title+"</span>" +
  "<span data-id=\""+oid+"\" class=\"actions pull-right \">" +
  "<span class=\"item-closed\"></span>" +
  "<span class=\"del-item\"></span>"+
  "</span></li>"
}

function delitem(item){

      var controllable = $($(item).parents('.controllable-items').first());
      var targetform =  $('#'+controllable.data('target'));
      var target = $(targetform.find('.controlled-items'));
      var itemtodel = $($(item).parents('.actions').first()).data('id');
      var event = jQuery.Event( "delItem" );
      var li = $(item).parents('li').first().remove();
      event.itemid = itemtodel;
      target.trigger(event)

}
$(document).ready(function(){

  $('.del-item').on('click', function(){
     delitem(this)
  });

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
            selectedItems.push(String(event.itemid));   // I used "WA" here to test.
            $(this).select2("val", selectedItems);
         }
  });


   $('.new-idea-control').click(function(){
        var form = $($(this).parents('form').first());
        if (this.checked) {
            form.find('.new-idea-form').removeClass('hide-bloc');
            $(form.find('.search-idea-form')).find('.select2-offscreen').select2("enable", false);
            //form.find('.search-idea-form').addClass('hide-bloc');
            
        }else{
            form.find('.new-idea-form').addClass('hide-bloc');
            $(form.find('.search-idea-form')).find('.select2-offscreen').select2("enable", true);
            //form.find('.search-idea-form').removeClass('hide-bloc');
        }
    });



    $(document).on('click','.add-idea-form button.ajax-button', function( event ) {
        var button = $(this);
        var form = $(button.parents('form.add-idea-form').first());
        var ideas_managment = $($(form).parents('.panel-body').first());
        var related_ideas = $(ideas_managment.find('ul.controllable-items'));
        var isnewidea = $(form.find('.new-idea-control'))[0].checked;
        var targetform =  $('#'+related_ideas.data('target'));
        var target = $(targetform.find('.controlled-items'));
        if (isnewidea)
         {
            newideaform = form.find('.new-idea-form');
            //POST dict
            var dict_post = {'title': newideaform.find('input[name="title"]').val(),
                             'description': newideaform.find('textarea[name="description"]').val(),
                             'keywords': $(newideaform.find('select[name="keywords"]')).select2('val')};
            var url = $(form).data('url');
            button.addClass('disabled');
            $.get(url, dict_post, function(data) {
               button.removeClass('disabled'); 
               related_ideas.append(get_tag(data['oid'], data['title']));
               item = $(related_ideas.find('span[data-id=\"'+data['oid']+'\"]')).find('.del-item');
               $('.del-item').on('click', function(){
                   delitem(this)
                });
               var event = jQuery.Event( "AddItem" );
               event.itemid = data['oid'];
               event.itemtitle = data['title'];
               target.trigger(event)
               //@TODO Gestion des erreurs
               
               //add to related ideas
             });


         }else{

         }
   });

});
