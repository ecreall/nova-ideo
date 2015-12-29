

function get_new_canvas(id){
      return "<canvas id=\""+id+"\"></canvas>"
}

$(document).on('submit','.analytics-form', function( event ) {
        var button = $(this).find('button').last();
        var parent = $($(this).parents('.tab-pane').first());
        var url = $(event.target).data('url');
        $(button).addClass('disabled');
        var values = $(this).serialize()+'&'+button.val()+'='+button.val();
        $.post(url, values, function(data) {
            if (data){
                $(parent.find('#chart-script')).html(data['body']);
                $(parent.find('.analytics-container .canvas-title')).removeClass('hide-bloc')
            };
             $(button).removeClass('disabled');
        });
        event.preventDefault();
});
