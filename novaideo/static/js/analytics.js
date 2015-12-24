

var legendTemplate = "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"

function get_new_canvas(id){
      return "<canvas id=\""+id+"\"></canvas>"
}

$(document).on('submit','.idea-by-keywords', function( event ) {
        var button = $(this).find('button').last();
        var url = $(event.target).data('url');
        $(button).addClass('disabled');
        var values = $(this).serialize()+'&'+button.val()+'='+button.val();
        $.post(url, values, function(data) {
            if (data){
                $('#chart-script').html(data['body']);
            };
             $(button).removeClass('disabled');
        });
        event.preventDefault();
});

  