;(function(){
	var NovaIdeoGuideline = window.NovaIdeoGuideline = window.NovaIdeoGuideline || {};

	NovaIdeoGuideline.init = function(){
		var tour_container = $('#novaideo-guide-tour-container');
		NovaIdeoGuideline.logo_url = 'https://www.nova-ideo.com/static/images/novaideoL.png';
        NovaIdeoGuideline.update_url = tour_container.data('update_url');
        NovaIdeoGuideline.guide = tour_container.data('guide');
        NovaIdeoGuideline.guide_value = parseInt(tour_container.data('guide_value'));
        NovaIdeoGuideline.page = tour_container.data('page');
        NovaIdeoGuideline.page_value = parseInt(tour_container.data('page_value'));
        guide_state = tour_container.data('guide_state');
        NovaIdeoGuideline.guide_state = guide_state? guide_state: 'first_start';
        if(NovaIdeoGuideline.guide_state != 'first_start' && NovaIdeoGuideline.guide && !isNaN(NovaIdeoGuideline.guide_value)){
	        $.cookie("guideline_"+NovaIdeoGuideline.guide, NovaIdeoGuideline.guide_value)
	        if(NovaIdeoGuideline.page && !isNaN(NovaIdeoGuideline.page_value) && NovaIdeoGuideline.page_value>0){
	            $.cookie("guideline_"+NovaIdeoGuideline.guide+'_'+NovaIdeoGuideline.page,  NovaIdeoGuideline.page_value)
	        }
        }

	};

	NovaIdeoGuideline.onStepShown = function(step){
		if(NovaIdeoGuideline.update_url){
	        var guide = step.guide.getName();
	     	var page = step.page.getName();
	     	var guide_value = parseInt($.cookie("guideline_"+guide));
	     	guide_value = isNaN(guide_value)? -1: guide_value;
	     	var page_value = parseInt($.cookie("guideline_"+guide+"_"+page));
	     	page_value = isNaN(page_value)? 0: page_value;
	     	var nextStep = step.guide.getNextStep();
	     	var page_state = 'pending'
	     	if(nextStep == null){
	     		page_state = 'complete'
	     	};
	     	NovaIdeoGuideline.guide = guide;
	     	NovaIdeoGuideline.guide_value = guide_value;
	     	NovaIdeoGuideline.page = page;
	     	NovaIdeoGuideline.page_value = page_value;
	     	NovaIdeoGuideline.page_state = page_state;
	     	$.post(
	     		NovaIdeoGuideline.update_url,
	     		{guide, guide_value, page, page_value, page_state}
	     	)
	    }
	};

	NovaIdeoGuideline.onSkip = function(guide_){
		if(NovaIdeoGuideline.update_url){
	        var guide = guide_.getName();
	        NovaIdeoGuideline.guide_state = 'skipped';
	     	$.post(
	     		NovaIdeoGuideline.update_url,
	     		{guide_state: NovaIdeoGuideline.guide_state}
	     	)
     	}
	};

	NovaIdeoGuideline.start = function(guide, page){
	  var current_guide = Guideline.getGuide(guide);
	  var current_page = current_guide? current_guide.getPageByName(page): null;
	  if (current_page){
	  	   current_guide.on('skip', function(this_){
                NovaIdeoGuideline.onSkip(this_)
           })
	      var steps = current_page.getSteps();
	      $.each(steps, function(index){
             var step = steps[index];
             step.on('show', function(this_){
                NovaIdeoGuideline.onStepShown(this_)
             })
	      })
		  var current_page_str = $.cookie("guideline_"+guide);
		  if(current_page_str == undefined){
		      Guideline.setCurrentPage(page); 
		      Guideline.getGuide(guide).start();
		  }else if(current_page_str != "skipped"){
		    var current_step = parseInt($.cookie("guideline_"+guide+"_"+page));
		    if(isNaN(current_step) || current_step <= steps.length){
		        var indicator = $('<div class="tour-indicator"/>')
		        var showAt = isNaN(current_step)? $('.contextual-help-toggle'): $(steps[current_step].showAt);
		        showAt.append(indicator);
		        var left = showAt.outerWidth()/2;
		        var top = showAt.outerHeight()/2;
		        indicator.css({
		            left: left,
		            top: top
		        });

		        left_marg = window.outerWidth - (indicator.offset().left + 80)
		        left = left_marg<=0? '-20px': left;
		        indicator.css({
		            left: left
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