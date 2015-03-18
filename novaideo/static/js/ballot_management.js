
$(document).ready(function(){
	$('.vote-action').on('click', function(){
       var modal = $($($(this).parents('.panel-body').first()).find('#vote-actions-modal').first());
       modal.modal('show');
	});

    $(document).on('submit','.vote-form', function( event ) {
        var formid = $(this).attr('id');

        var button = $(event.originalEvent.explicitOriginalTarget);
        if (button.val() == 'Cancel'){
            var modal = $($(this).parents('#vote-actions-modal').first());
            modal.modal('hide');
        	event.preventDefault();
        }
   });
})