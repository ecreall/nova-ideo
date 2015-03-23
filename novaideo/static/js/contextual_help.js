

function init_contextual_help(){
	var helps = $('.contextual-help');
	for(var i=0; i<helps.length; i++){
		var help = $(helps[i]);
        help.data('top', help.offset().top);
        if($('.principal-help').length == 0){  
            help.addClass('hide-bloc');
        }
    }
}

$(document).ready(function(){
	init_contextual_help();

    $('div.panel-collapse').on('shown.bs.collapse', function(){
        var help = $('.'+ $(this).data('help'));
        if(help.length>0){
            var helps = $('.contextual-help-item');
            var help_parent = $(help.parents('.contextual-help.alert').first());
            var position = $(this).offset().top;
            helps.addClass('hide-bloc');
            help_parent.removeClass('hide-bloc');
            help_parent.offset({top: position});
            help.removeClass('hide-bloc');
	        
        }
    });

    $('div.panel-collapse').on('hide.bs.collapse', function(){
        var help = $('.'+ $(this).data('help'));
        var principal_help = $('.principal-help');
        if(help.length>0){
            var helps = $('.contextual-help-item');
            var help_parent = $(help.parents('.contextual-help.alert').first());
            helps.addClass('hide-bloc');
            if(principal_help.length>0){
              help_parent.offset({top: parseInt(help_parent.data('top'))});
              principal_help.removeClass('hide-bloc')
            }else{
              help_parent.addClass('hide-bloc');
            }
            
        }
    })
})