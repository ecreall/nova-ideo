

function get_new_canvas(id){
      return "<canvas id=\""+id+"\"></canvas>"
}

$(document).on('submit','.content-by-keywords', function( event ) {
        var button = $(this).find('button').last();
        var url = $(event.target).data('url');
        $(button).addClass('disabled');
        var values = $(this).serialize()+'&'+button.val()+'='+button.val();
        $.post(url, values, function(data) {
            if (data){
                $('#chart-script').html(data['body']);
                $('.analytics-keywords-container .canvas-title').removeClass('hide-bloc')
            };
             $(button).removeClass('disabled');
        });
        event.preventDefault();
});

$(document).on('submit','.content-by-states', function( event ) {
        var button = $(this).find('button').last();
        var url = $(event.target).data('url');
        $(button).addClass('disabled');
        var values = $(this).serialize()+'&'+button.val()+'='+button.val();
        $.post(url, values, function(data) {
            if (data){
                $('#chart-script').html(data['body']);
                $('.analytics-states-container .canvas-title').removeClass('hide-bloc')
            };
             $(button).removeClass('disabled');
        });
        event.preventDefault();
});
  