
function generate_analytics_alert(){
    var result = "<div class=\"alert alert-warning\">"+
    novaideo_translate("Aucune valeur n'est trouvée!")+
    "</div>"
    return result
}


function generate_analytics_study(values){

    var result =  "<div class=\"alert alert-info\">"+
    novaideo_translate("Ces graphiques sont produits à partir d'un échantillon présentant:")+
    "<ul class=\"list-unstyled\">";
    for(key in values) {
        result += "<li>";
        if(values[key]>1){
             result += values[key]+ novaideo_translate(" contenus de type ")+ key;
        }else{
             result += values[key]+ novaideo_translate(" contenu de type ")+ key;
        }
        result += "</li>"
    };

    result += "</ul></div>"
    return result
}

function get_new_canvas(id){
      return "<canvas id=\""+id+"\"></canvas>"
}

$(document).on('submit','.analytics-form', function( event ) {
        var button = $(this).find('button').last();
        var parent = $($(this).parents('.tab-pane').first());
        var url = $(event.target).data('url');
        $(button).addClass('disabled');
        var values = $(this).serialize()+'&'+button.val()+'='+button.val();
        $(parent.find('.analytics-container .loading-indicator')).removeClass('hide-bloc')
        $.post(url, values, function(data){
            if (data){
                $(parent.find('#chart-script')).html(data['body']);
                var script = $(parent.find('#chart-script script').first());
                if(script.data('has_value')){
                    $(parent.find('.analytics-container .canvas-title')).removeClass('hide-bloc')
                }else{
                    $(parent.find('.analytics-container .canvas-title')).addClass('hide-bloc');
                    $(parent.find('.analytics-container .legend')).html('');
                    var charts = $(parent.find('.chart-container'));
                    charts.removeClass('object-well');
                    charts.removeClass('well');
                    for(var i=0; i<charts.length; i++){
                        var chart = $(charts[i]);
                        var canvas = chart.find('canvas');
                        var ctx = canvas.get(0).getContext("2d");
                        ctx.clearRect(0, 0, 1500, 1500);
                        var new_canvas = get_new_canvas($(canvas).attr('id'));
                        $(canvas).replaceWith(new_canvas)
                    }
                }
            };
            $(button).removeClass('disabled');
            $(parent.find('.analytics-container .loading-indicator')).addClass('hide-bloc')
        });
        event.preventDefault();
});
