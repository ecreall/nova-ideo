;(function(){
	var NovaIdeoGuideline = window.NovaIdeoGuideline = window.NovaIdeoGuideline || {};

	NovaIdeoGuideline.start = function(guide, page){
	  var current_guide = Guideline.getGuide(guide);
	  var current_page = current_guide? current_guide.getPageByName(page): null;
	  if (current_page){
		  var current_page_str = $.cookie("guideline_"+guide);
		  if(current_page_str == undefined){
		      Guideline.setCurrentPage(page); 
		      Guideline.getGuide(guide).start();
		  }else if(current_page_str != "skipped"){
		    var current_step = parseInt($.cookie("guideline_"+guide+"_"+page));
		    var steps = current_page.getSteps().length;
		    if(isNaN(current_step) || current_step <= steps){
		        var indicator = $('<div class="tour-indicator"/>')
		        var showAt = isNaN(current_step)? $('.contextual-help-toggle'): $(current_page.getSteps()[current_step].showAt);
		        showAt.append(indicator);
		        var left = showAt.outerWidth()/2;
		        var top = showAt.outerHeight()/2;
		        indicator.css({
		            left: left,
		            top: top
		        });
		        showAt.on('mouseover', function(){
	                Guideline.setCurrentPage(page); 
	                Guideline.getGuide(guide).start();
	                $('.tour-indicator').remove()
	            })
		    }
		  }
	  }
	};

    NovaIdeoGuideline._ = novaideo_translate;

	NovaIdeoGuideline.next_btn = "<button type='button' class='btn btn-xs btn-primary'>"+
                      "<span class='glyphicon glyphicon-forward' aria-hidden='true'></span> "+
                      NovaIdeoGuideline._("Next")+
                    "</button>";

    NovaIdeoGuideline.prev_btn = "<button type='button' class='btn btn-xs btn-primary'>"+
                      "<span class='glyphicon glyphicon-backward' aria-hidden='true'></span> "+
                      NovaIdeoGuideline._("Previous")+
                    "</button>";

    NovaIdeoGuideline.end_btn = "<button type='button' class='btn btn-xs btn-success'>"+
                      "<span class='glyphicon glyphicon-ok' aria-hidden='true'></span> "+
                      NovaIdeoGuideline._("End")+
                    "</button>";

    NovaIdeoGuideline.stepControlContainer = "<div class='btn-group btn-group-xs step-control-container'/>";

})();