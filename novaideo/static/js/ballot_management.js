$(document).on('submit','.vote-form', function( event ) {
    var formid = $(this).attr('id');

    var button = $(event.originalEvent.explicitOriginalTarget);
    if (button.val() == 'Cancel'){
        var modal = $($(this).parents('#vote-actions-modal').first());
        modal.modal('hide');
    	event.preventDefault();
    }
});

function show_votes_modal(id){
    var modal_container = $('.votes-modal-container')
    modal_container.data('source', id)
    modal_container.attr('class', 'modal-l votes-modal-container modal fade')
    var action_body = '<div id="panel-actions-vote" class="panel-group">'+
                      jQuery.parseJSON($('#'+id).data('body')) + '</div>';
    $(modal_container.find('.modal-body')).html(action_body);
    $(modal_container.find('.modal-title')).text('Votes')
    try {
      deform.processCallbacks();
    }catch(err) {};
    modal_container.css('opacity', '1')
    modal_container.modal('show');
    $($('#panel-actions-vote').find("a.panel-title").first()).click();
}

$(document).on('click', '.vote-action', function(){
    var id = $(this).parents('.content-view').first().find('.vote-actions-container').attr('id')
    show_votes_modal(id)
});
