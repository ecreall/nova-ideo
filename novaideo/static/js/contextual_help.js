

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

$(document).on('click', '.nav-tabs>li', function(){
    var $this = $(event.target).parents('li').first()
    if ($this.data('help')){
        var help = $('.'+ $this.data('help'));
        if(help.length>0){
            var helps = $('.contextual-help-item');
            var help_parent = $(help.parents('.contextual-help').first());
            helps.addClass('hide-bloc');
            help_parent.removeClass('hide-bloc');
            help.removeClass('hide-bloc');
        }
        
    }else{
        var principal_help = $('.principal-help');
        if(principal_help.length>0){
            var helps = $('.contextual-help-item');
            helps.addClass('hide-bloc');
            principal_help.removeClass('hide-bloc')
        }
    }
});

$(document).ready(function(){
    init_contextual_help();
})