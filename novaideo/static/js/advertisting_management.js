var open_template = "<span class=\"content-control pull-right glyphicon glyphicon-chevron-up\"></span>"
var close_template = "<span class=\"content-control pull-right glyphicon glyphicon-chevron-down\"></span>"


function html_content_is_empty(content){
	return (content.val() == "<p><br data-mce-bogus=\"1\"></p>" || 
  	        content.val() == "")
}

function init_label(content, content_class, opposit_class, template){
    var label = $(content.find('label').first());
	label.after(template);
	var icon = $(content.find('.glyphicon').first());
	icon.on('click', function(event){
		var inner = $(content.find('.'+content_class).first());
		if(content.hasClass('closed')){
           inner.slideDown( );
           content.removeClass('closed');
           $(this).removeClass('glyphicon-chevron-down');
           $(this).addClass('glyphicon-chevron-up');
           
		}else{
           inner.slideUp( );
           content.addClass('closed');
           $(this).removeClass('glyphicon-chevron-up');
           $(this).addClass('glyphicon-chevron-down');
		};
		if (!event.stop){
		   var click = jQuery.Event("click");
           click.stop = true;
		   $($(this).parents('form').first().find('.'+opposit_class+' span.content-control').first()).trigger(click)
		}
	})
}

function init_html_content(){
    var html_contents = $('.advertising-html-content');
    for(var i=0; i<html_contents.length; i++){
    	var content = $(html_contents[i]);
    	var template = close_template;
    	if(html_content_is_empty($(content.find('.html-content-text').first()))){
    	   content.addClass('closed');
    	   template = open_template;
        };
    	init_label($(html_contents[i]), 'mce-tinymce.mce-container', 'advertising-file-content', template);
    };

};

function init_file_content(){
	var file_contents = $('.advertising-file-content');
	for(var i=0; i<file_contents.length; i++){
        var content = $(file_contents[i]);
        var opposit_is_closed = html_content_is_empty($(content.parents('form').first().find('.advertising-html-content .html-content-text').first()));
        var template = close_template;
    		if(!opposit_is_closed){
               content.addClass('closed');
               var inner = $(content.find('.file-content').first());
               inner.css('display', 'none');
               template = open_template;
    		};
        init_label($(file_contents[i]), 'deformFileupload', 'advertising-html-content', template)
  }
};


function set_preview_template(target, e){
	var preview = flash_preview;
	target.after(preview);
	// var img = $('img.file-content-preview')
	// img.attr('src', e.target.result);
	// img.removeClass('hide-bloc');
    var img = $('embed.file-content-preview');
    var param = $('param.file-content-preview-param');
    var result = e.target.result;
    img.attr('src', result);
    param.attr('value', result);
}

var ui_prototype = "<div class=\"preview-ui\">"+
                    "<div  class=\"preview-usermenu\">"+
                      "</div>"+
                    "<div class=\"preview-menu\"></div>"+
                    "<div class=\"preview-right-ui\">"+
                          "<div class=\"preview-advertising-right-top-1\"></div>"+
                          "<div class=\"preview-advertising-right-top-2\"></div></div>"+
                      "</div>"

var panels_css_mapping = {
  'advertisting_right_1': 'preview-advertising-right-top-1',
  'advertisting_right_2': 'preview-advertising-right-top-2'
}

function set_active_preview(input, preview){
    var values = input.val();
    if(values){
      for(var i=0; i<values.length; i++){
        var css_class = panels_css_mapping[values[i]];
        $(preview.find('.'+css_class)).addClass('preview-advertising-active')

      }
  }
};

function synchronize_ui_preview(){
      var form = $($(this).parents('form').first());
      var old_preview = $(form.find('.preview-ui').first());
      $(old_preview.find('.preview-advertising-active')).removeClass('preview-advertising-active');
      var input_positions = $(form.find('.advertising-positions').first());
      var position_form_group = $(input_positions.parents('.form-group').first());
      set_active_preview(input_positions, old_preview);
};

function add_ui_preview(){
    var inputs = $('.advertising-positions');
    for(var i=0; i<inputs.length; i++){
      var input_positions = $(inputs[i]);
      var position_form_group = $(input_positions.parents('.form-group').first());
      position_form_group.css('width', '75%');
      position_form_group.after(ui_prototype);
      var form = $(input_positions.parents('form').first());
      var preview = $(form.find('.preview-ui').first());
      set_active_preview(input_positions, preview);
    }
};

$(document).ready(function(){
  add_ui_preview();

  $(".advertising-positions").on('change', synchronize_ui_preview);

  init_html_content();
  
  init_file_content();

  $('.html-content-text').on('ed_init', function(e){
  	  if(html_content_is_empty($(this))){
          var mce_container = $($(this).parents('.advertising-html-content').first().find('.mce-tinymce.mce-container').first());
          mce_container.css('display', 'none');
      }
  });

});

