function get_option(data){
    return "<option value=\""+data['value']+"\" selected=\"selected\" >"+data['content']+"</option>"
}

function add_option(select, option){
    var id = $(option).data('item');
    var oldoption = $($(select).find('option[value=\''+id+'\']'))
    if (oldoption.length>0){
       $(oldoption[0]).attr('selected', 'selected')
    }else{
       $(select).append(get_option({'value':id, 'content':id}));
    }
}


function remove_option(select, option){
    var id = $(option).data('item');
    var oldoption = $($(select).find('option[value=\''+id+'\']'))
    if (oldoption.length>0){
       $(oldoption[0]).removeAttr('selected')
    }
}


function mouseout_item(){
   $('.select-container').removeClass('selected-container');
}


function dragstart(e){
    var dataTransfer = e.originalEvent.dataTransfer;
    dataTransfer.effectAllowed = 'copy';
    dataTransfer.setData('Text', $(this).text());
    dataTransfer.setData('id', this.id);
    dataTransfer.setData('item', $(this).attr('data-item'));
    var source = $(e.currentTarget);
    var explanation_containers = $('.select-container');
    var draggedId = this.id;
    var itemid = $(this).attr('data-item');
    $(this).bind('mouseout', mouseout_item);
    for (d=0; d< explanation_containers.length; d++){
        var target = $(explanation_containers[d]);
        //if (exists_constraint(target, draggedId, itemid, global_id )){
           target.addClass('selected-container');
        //};
    };
};


function dragover(e){
    var event = e.originalEvent;
    if (event.preventDefault) {
        event.preventDefault();
    }

    var dataTransfer = event.dataTransfer;
    var draggedId = dataTransfer.getData('id');
    var itemid = dataTransfer.getData('item');
    var draggedElement = $('#' + draggedId);
    var draggedText = draggedElement.text();
    var target = $(e.currentTarget);
//       target.addClass('exists-item');
       target.addClass('not-exists-item');
    event.dataTransfer.dropEffect = 'copy';
    return false;
};


function dragleave(e) {
    var event = e.originalEvent;
    if (event.preventDefault) {
        event.preventDefault();
    }
    var target = $(e.currentTarget);
    target.removeClass("exists-item");
    target.removeClass("not-exists-item");
    //$('.explanation-container').removeClass('selected-container');
}


function dragEnd(e) {
    var dataTransfer = e.originalEvent.dataTransfer;
    dataTransfer.effectAllowed = 'copy';
    dataTransfer.setData('Text', $(this).text());
    dataTransfer.setData('id', this.id);
    var source = $(e.currentTarget);
    $('.select-container').removeClass('selected-container');
}


function drop(e){
    var event = e.originalEvent;
    if (event.stopPropagation) {
        event.stopPropagation();
    }
    var dataTransfer = event.dataTransfer;
    var draggedId = dataTransfer.getData('id');
    var draggedElement = $('#' + draggedId);
    var target = $(e.currentTarget);
    $('.select-container').removeClass('selected-container');
    var targetselect = $(target.parents('.form-group').first()).find('select').first();
    var oldselect = $(draggedElement.parents('.form-group').first()).find('select').first();
    add_option(targetselect, draggedElement);
    remove_option(oldselect, draggedElement)
    $(target).append(draggedElement);
    target.removeClass("not-exists-item");
    init_remove_button()
    return false;
};

function init_dragdropselect(seqadd){
  var element = ($(seqadd).parents('.panel').first()).find('.select-container').last();
  $(element).on('dragover', dragover);
 
  $(element).on('drop', drop);

  $(element).on('dragleave', dragleave);

  $(element).on('dragEnd', dragEnd);

}

function init_remove_button(){
  var removeactions = $('.remove-item');
  for (i=0; i<removeactions.length; i++){
    var seqremove = removeactions[i];
    var element = ($(seqremove).parents('.sequence-item').first()).find('.select-container').last();
    if ($(element).find('.select-item').length >0){
       $(seqremove).removeClass('remove-item');
       $(seqremove).addClass('disabled-remove-item');
       $(seqremove).attr('onclick', 'javascript:return false')
       
     }
 };

  var disabledremoveactions = $('.disabled-remove-item');
  for (i=0; i<disabledremoveactions.length; i++){
    var seqremove = disabledremoveactions[i];
    var element = ($(seqremove).parents('.sequence-item').first()).find('.select-container').last();
    if ($(element).find('.select-item').length == 0){
       $(seqremove).removeClass('disabled-remove-item');
       $(seqremove).addClass('remove-item');
       $(seqremove).attr('onclick', "javascript:deform.removeSequenceItem(this);")
     }
 };
}

$(document).ready(function(){

  $('.select-item').on('dragstart', dragstart);
 
  $('.select-container').on('dragover', dragover);
 
  $('.select-container').on('drop', drop);

  $('.select-container').on('dragleave', dragleave);

  $('.select-container').on('dragEnd', dragEnd);

   $('.explanation-amendment .global-action').on('click', function(){
        var explanation_items = $($(this).parents('.explanation-amendment').first()).find('.items-control').first();
        if (explanation_items.hasClass('hide-bloc')) {
            explanation_items.removeClass('hide-bloc')           
        }else{
            explanation_items.addClass('hide-bloc')
        }
    });
 
  init_remove_button();

});
