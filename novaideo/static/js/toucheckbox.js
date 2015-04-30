function init_terms_of_use(formid){
  var form = $($(formid).parents('form').first());
  form.on('submit',function( event ) {
        var commentmessagedanger = $(this).find('#messagedanger');
        var input = $($($(event.target).children().filter('fieldset')[0]).find('input[type|="checkbox"][name|="accept_conditions"]').first());
        var button = $(event.originalEvent.explicitOriginalTarget);
        if (button.val() !== 'Cancel'){
	        if(!input.prop('checked')){
	            event.preventDefault();
	            $( commentmessagedanger).text( "Il faut accepter les conditions d'utilisation" ).show();
	        }
	    }
   });
}
