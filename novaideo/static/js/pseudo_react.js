function nav_bar_component(data){
	var components = $('[data-component_type="navbar_component"]')
	var components_to_update = components.map(function(){
		if($.inArray($(this).attr('id'), data['counters-to-update']) >= 0){
			return $(this)
		}
	})
	
	$.each(components_to_update, function(index){
		var original_components = $(this)
		var component_id = original_components.attr('id')
		if (original_components.length > 0){
			var original_component = $(original_components[0])
			var new_component = null
			if (data[component_id+'.item_nb'] > 0){
				new_component = '<li data-component_type="navbar_component" class="menu-item counter" id="'+component_id+'">'
	            var ori_view_link =  $(original_component.find('a').first())
	            if (ori_view_link && ori_view_link.attr('href')){
	              var link_class = ori_view_link.attr('class')? ori_view_link.attr('class'): ''
	              new_component += '<a class="'+link_class+'" href="'+data[component_id+'.url']+'">'
	            	
	            }else{
	            	new_component += '<a href="'+data[component_id+'.url']+'">'
	            }
			    new_component +='<span class="hidden-xs">'+data[component_id+'.title']+' <span class=" item-nb">'+data[component_id+'.item_nb']
                    if (data[component_id+'.all_item_nb']){
                    	new_component += '/'+data[component_id+'.all_item_nb']
                    }
			    new_component +='</span></span>'
			    new_component +='<span class="visible-xs-inline-block action-icon '+data[component_id+'.icon']+'"></span>'
			    new_component +='</a>'
			    new_component +='</li>'
			}else{
				new_component = '<li data-component_type="navbar_component" class="menu-item counter" id="'+component_id+'">'
	            new_component += '<a class="disabled">'
	            new_component +='<span class="hidden-xs">'+data[component_id+'.title']+'</span>'
			    new_component +='<span class="visible-xs-inline-block action-icon '+data[component_id+'.icon']+'"></span>'
			    new_component +='</a>'
			    new_component +='</li>'
			}
			if(new_component != null){
				original_component.replaceWith($(new_component))
			}
			
		}
	})
}


function novaideo_content_nb_component(data){
	var components = $('[data-component_type="novaideo_content_nb"]')
	var components_to_update = components.map(function(){
		if($.inArray($(this).attr('id'), data['counters-to-update']) >= 0){
			return $(this)
		}
	})
	$.each(components_to_update, function(index){
		var original_components = $(this)
		var component_id = original_components.attr('id')
		if (original_components.length > 0){
			var original_component = $(original_components[0])
			var new_component = null
			if (data[component_id+'.item_nb'] > 0){
				new_component = '<li data-component_type="novaideo_content_nb" class="counter" id="'+component_id+'"><strong>'
				new_component += data[component_id+'.item_nb'] + '</strong> <span>'+ data[component_id+'.title'] + '</span></li>'
			}else{
				new_component = '<li data-component_type="novaideo_content_nb" class="counter" id="'+component_id+'"><li>'
			}
			if(new_component != null){
				original_component.replaceWith($(new_component))
			}
			
		}
	})
}

function tab_component_component(data){
	var components = $('[data-component_type="tab_component"]')
	var components_to_update = components.map(function(){
		if($.inArray($(this).attr('id'), data['counters-to-update']) >= 0){
			return $(this)
		}
	})
	$.each(components_to_update, function(index){
		var original_components = $(this)
		var component_id = original_components.attr('id')
		if (original_components.length > 0){
			var original_component = $(original_components[0])
			$(original_component.find('>a>span').last()).text(data[component_id+'.title'])
		}
	})
}


function footer_action_component(data){
	$.each(data.components, function(index){
		var component_id = 'component-footer-action-'+data.components[index]
		var original_components = $('[id="'+component_id+'"]')
		var actionlinks = $(original_components.parents('a.ajax-action'))
		$.each( original_components, function(index){
			var original_component = $(original_components[index])
			var new_component_id = data.has_opposit? 'component-footer-action-'+data.new_component_id:component_id
			var new_component = '<span id="'+new_component_id+'"><span class="footer-icon '+data.action_icon+'"></span> '+
			                    '<span class="hidden-xs"> '+data.action_title+' ('+data.action_item_nb+')</span></span>'
			if(new_component != null){
				original_component.replaceWith($(new_component))
				if (data.has_opposit){
                    $.each(actionlinks, function(actionindex){
                    	$(this).attr('data-actionid', data.opposit_action_id)
                    	$(this).attr('data-updateurl', data.opposit_actionurl_update)
                    	$(this).attr('data-after_exe_url', data.opposit_actionurl_after)
                    	$(this).attr('data-title', data.action_title)
                    	$(this).attr('data-view_title', data.action_view_title)
                    	$(this).attr('data-icon', data.action_icon)

                    	$(this).data('actionid', data.opposit_action_id)
                    	$(this).data('updateurl', data.opposit_actionurl_update)
                    	$(this).data('after_exe_url', data.opposit_actionurl_after)
                    	$(this).data('title', data.action_title)
                    	$(this).data('view_title', data.action_view_title)
                    	$(this).data('icon', data.action_icon)

                    	$(this).attr('title', data.action_title)
                    	$(this).attr('id', data.opposit_action_id+'-btn')
                    })
				}

			}
		})
	})
}

function dropdown_action_component(data){
	$.each(data.components, function(index){
		var component_id = 'component-dropdown-action-'+data.components[index]
		var original_components = $('[id="'+component_id+'"]')
		var actionlinks = $(original_components.parents('a.ajax-action'))
		$.each( original_components, function(index){
			var original_component = $(original_components[index])
			var new_component_id = data.has_opposit? 'component-dropdown-action-'+data.new_component_id:component_id
			var new_component = '<span id="'+new_component_id+'"><span class="'+data.action_icon+'"></span> '+
			                    data.action_title+'</span>'
			if(new_component != null){
				original_component.replaceWith($(new_component))
				if (data.has_opposit){
                    $.each(actionlinks, function(actionindex){
                    	$(this).attr('data-actionid', data.opposit_action_id)
                    	$(this).attr('data-updateurl', data.opposit_actionurl_update)
                    	$(this).attr('data-after_exe_url', data.opposit_actionurl_after)
                    	$(this).attr('data-title', data.action_title)
                    	$(this).attr('data-view_title', data.action_view_title)
                    	$(this).attr('data-icon', data.action_icon)

                    	$(this).data('actionid', data.opposit_action_id)
                    	$(this).data('updateurl', data.opposit_actionurl_update)
                    	$(this).data('after_exe_url', data.opposit_actionurl_after)
                    	$(this).data('title', data.action_title)
                    	$(this).data('view_title', data.action_view_title)
                    	$(this).data('icon', data.action_icon)

                    	$(this).attr('title', data.action_title)
                    	$(this).attr('id', data.opposit_action_id+'-btn')
                    })
				}

			}
		})
	})
}

function view_title_component(data){
    var url = window.location.href; 
	var concerned_view = url.indexOf('/'+data.view_name+'')>=0 || url.indexOf('/@@'+data.view_name)>=0  
	if(data.view_title && concerned_view){
		$($('.pontus-main .panel-title>h4').first()).text(data.view_title)
	}
}

function list_items_component(data){
    var url = window.location.href; 
	var concerned_view = url.indexOf('/'+data.view_name+'')>=0 || url.indexOf('/@@'+data.view_name)>=0   
	if(data.removed && (data.force_remove || concerned_view)){
        data.search_item.fadeOut( 1000 );
        return
	}
    if(data.new_obj_body){
        data.search_item.replaceWith(data.new_obj_body)
        try {
            deform.processCallbacks();
        }catch(err) {};
	}

}


function list_channels_component(data){
	if(data.removed && data.channel_item){
        var channel_len = $(data.channel_item.parents('.channels-block').find('.channel-title .channel-len').first())
		var nb = parseInt(channel_len.text().replace('(', '').replace(')', ''))-1
		channel_len.text('('+nb+')')
		data.channel_item.fadeOut( 1000 );
	}
	if(!data.removed && data.new_components.length>0 && data.channels_target.length>0){
		var new_components = $(data.new_components[0])
		$(new_components.find('a.channel-action')).addClass('activated')
	    data.channels_target.append(new_components)
		var channel_len = $(data.channels_target.parents('.channels-block').find('.channel-title .channel-len').first())
		var nb = parseInt(channel_len.text().replace('(', '').replace(')', ''))+1
		channel_len.text('('+nb+')')
		
	}
}

function redirect_component(data){
	if (data.redirect_url){
		 window.location.replace(data.redirect_url)
    }
}

function alert_component(data){
	if (data.alert_msg){
		if(data.alert_source){
			data.alert_source.notify(
	            data.alert_msg,
	            {
	              globalPosition: 'top center',
	              className: data.alert_type,
	            });
		}else{
			$.notify(
	            data.alert_msg,
	            {
	              globalPosition: 'bottom center',
	              className: data.alert_type,
	            });
		}
    }
}


var pseudo_react_components = {
	'support_action': [nav_bar_component, view_title_component,
	                   list_items_component, alert_component,
	                   tab_component_component, novaideo_content_nb_component],
	'footer_action': [nav_bar_component, footer_action_component,
	                  view_title_component, list_items_component,
	                  alert_component, novaideo_content_nb_component,
	                  tab_component_component],
	'redirect_action': [nav_bar_component,redirect_component,
	                    list_items_component, novaideo_content_nb_component,
	                    view_title_component, alert_component,
	                    tab_component_component],
	'dropdown_action': [dropdown_action_component, list_channels_component,
	                    alert_component]
}

function update_components(data){
    var actionid = data.action_id
    var components_to_update = pseudo_react_components[actionid]
    $.each(components_to_update, function(index){
    	this(data)	
    })
}
