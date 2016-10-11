

function init_contextual_help(){
    if($(".contextual-help").length>0){
      $(".contextual-help-toggle").addClass('active');
      if($(".contextual-help-toggle").hasClass('toggled')){
        $(".contextual-help").addClass("toggled");
      }
    }
    var helps = $('.contextual-help');
    for(var i=0; i<helps.length; i++){
        var help = $(helps[i]);
        if($('.principal-help').length == 0){  
            help.addClass('hide-bloc');
        }
    }
}


$(document).on('click', ".contextual-help-toggle.active", function(e) {
    e.preventDefault();
    $(this).toggleClass("toggled");
    $(".contextual-help").toggleClass("toggled");
});

$(document).on('click', ".contextual-help-toggle-close", function(e) {
    e.preventDefault();
    $(".contextual-help-toggle").toggleClass("toggled");
    $(".contextual-help").toggleClass("toggled");
});

$(document).ready(function(){
    init_contextual_help();

    $('div.panel-collapse').on('shown.bs.collapse', function(){
        var help = $('.'+ $(this).data('help'));
        if(help.length>0){
            var helps = $('.contextual-help-item');
            var help_parent = $(help.parents('.contextual-help.alert').first());
            helps.addClass('hide-bloc');
            help_parent.removeClass('hide-bloc');
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
                principal_help.removeClass('hide-bloc')
            }else{
              help_parent.addClass('hide-bloc');
            }
            
        }
    })
})