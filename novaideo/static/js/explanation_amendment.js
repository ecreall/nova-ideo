function get_item(data){
    return "<span id=\""+data['id']+"\" class=\""+data['class']+"\" draggable=\"true\">"+data['content']+"</span>"
}

function get_idea(data){
    return "<span id=\""+data['id']+"\" class=\"label label-basic idea-item\" draggable=\"true\">"+data['title']+"</span>"
}


function container_constraint(source, target){
    if(source.indexOf("both")>=0 && target.indexOf("old")>=0){
        return true
    }
    if(source.indexOf("replaced")>=0 && (target.indexOf("deleted")>=0 || target.indexOf("old")>=0)){
        return true
    }
    if(source.indexOf("replacement")>=0 && (target.indexOf("added")>=0 || target.indexOf("old")>=0)){
        return true
    }
    return false

}

function dragstart(e){
    var dataTransfer = e.originalEvent.dataTransfer;
    dataTransfer.effectAllowed = 'copy';
    dataTransfer.setData('Text', $(this).text());
    dataTransfer.setData('id', this.id);
    dataTransfer.setData('itemid', $(this).attr('data-itemid'));
    var source = $(e.currentTarget);
};


function dragover(e){
    var event = e.originalEvent;
    if (event.preventDefault) {
        event.preventDefault();
    }

    var dataTransfer = event.dataTransfer;
    var draggedId = dataTransfer.getData('id');
    var itemid = dataTransfer.getData('itemid');
    var draggedElement = $('#' + draggedId+'[data-itemid=\''+itemid+'\']');
    var draggedText = draggedElement.text();
    var target = $(e.currentTarget);
    var global_id = draggedElement.data("globalid");
    var items = $(target).find('#' + draggedId+':not([data-itemid=\''+itemid+'\'])');
    var both_item = $(target).find('#'+global_id+'-both');
    var items_both = [];
    if (draggedId == global_id+'-both'){
       items_both = $(target).find('.explanation-item[data-globalid=\''+global_id+'\']');
    };
    if (items.length>0 || items_both.length>0 || both_item.length>0 || !container_constraint(draggedId, target.attr('id'))){
       target.addClass('exists-item')
    }else{
       target.addClass('not-exists-item')
    };
    event.dataTransfer.dropEffect = 'copy';
    return false;
};


function dragleave(e) {
    var event = e.originalEvent;
    if (event.preventDefault) {
        event.preventDefault();
    }
    var target = $(e.currentTarget);
    target.removeClass("exists-item")
    target.removeClass("not-exists-item")
}


function dragEnd(e) {
    var dataTransfer = e.originalEvent.dataTransfer;
    dataTransfer.effectAllowed = 'copy';
    dataTransfer.setData('Text', $(this).text());
    dataTransfer.setData('id', this.id);
    var source = $(e.currentTarget);
}


function drop(e){
    var event = e.originalEvent;
    if (event.stopPropagation) {
        event.stopPropagation();
    }
    var dataTransfer = event.dataTransfer;
    var draggedId = dataTransfer.getData('id');
    var itemid = dataTransfer.getData('itemid');
    var draggedElement = $('#' + draggedId+'[data-itemid=\''+itemid+'\']');
    var draggedText = draggedElement.text();
    var target = $(e.currentTarget);
    var global_id = draggedElement.data("globalid");
    var items = $(target).find('#' + draggedId+':not([data-itemid=\''+itemid+'\'])');
    var both_item = $(target).find('#'+global_id+'-both');
    var items_both = [];
    if (draggedId == global_id+'-both'){
       items_both = $(target).find('.explanation-item[data-globalid=\''+global_id+'\']');
    };
    if (items.length>0 || items_both.length>0 || both_item.length>0 || !container_constraint(draggedId, target.attr('id'))){
        target.removeClass("exists-item");
        return false
    }
    if (!draggedElement.hasClass('droped-item')){
        var clone = draggedElement.clone();
        clone.addClass("droped-item");
        $(target).append(clone);
        var itemid = parseInt(clone.data('itemid'));
        itemid += 1;
        clone.bind('dragstart', dragstart);
        draggedElement.attr('data-itemid', itemid);
        var parent = $($(target).parents('div.panel-heading').first());
        var data = {"title":parent.data("title"), "id":parent.data("id")};
        $(draggedElement.parents('.items-control').first()).find('#'+draggedElement.attr('id')+'-container').append(get_idea(data))
    }else{
        $(target).append(draggedElement);
    }
    target.removeClass("not-exists-item")
    return false;
};


$(document).ready(function(){

  $('.explanation-item').on('dragstart', dragstart);
 
  $('.explanation-container').on('dragover', dragover);
 
  $('.explanation-container').on('drop', drop);

  $('.explanation-container').on('dragleave', dragleave);

  $('.explanation-container').on('dragEnd', dragEnd);

   $('.explanation-amendment .global-action').on('click', function(){
        var explanation_items = $($(this).parents('.explanation-amendment').first()).find('.items-control').first();
        if (explanation_items.hasClass('hide-bloc')) {
            explanation_items.removeClass('hide-bloc')           
        }else{
            explanation_items.addClass('hide-bloc')
        }
    });


  //$('.explanation-item').on('dragstart', dragstart);
 
  $('.ideas-container').on('dragover', dragover);
 
  $('.ideas-container').on('drop', drop);

  $('.ideas-container').on('dragleave', dragleave);

  $('.ideas-container').on('dragEnd', dragEnd);
});
