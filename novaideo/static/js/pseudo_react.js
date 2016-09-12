function nav_bar_component(data){
	$.each(data.components, function(index){
		var component_id = 'component-navbar-'+data.components[index]
		var original_components = $('#'+component_id)
		if (original_components.length > 0){
			var original_component = $(original_components[0])
			var new_component = null
			if (data.navbar_item_nb > 0){
				new_component = '<li class="menu-item" id="'+component_id+'">'
	            var ori_view_link =  $(original_component.find('a').first())
	            if (ori_view_link && ori_view_link.attr('href')){
	              var link_class = ori_view_link.attr('class')? ori_view_link.attr('class'): ''
	              new_component += '<a class="'+link_class+'" href="'+data.view_url+'">'
	            	
	            }else{
	            	new_component += '<a href="'+data.view_url+'">'
	            }
			    new_component +='<span class="hidden-xs">'+data.navbar_title+' <span class=" item-nb">'+data.navbar_item_nb
                    if (data.navbar_all_item_nb){
                    	new_component += '/'+data.navbar_all_item_nb
                    }
			    new_component +='</span></span>'
			    new_component +='<span class="visible-xs-inline-block action-icon '+data.navbar_icon+'"></span>'
			    new_component +='</a>'
			    new_component +='</li>'
			}else{
				new_component = '<li class="menu-item" id="'+component_id+'">'
	            new_component += '<a class="disabled">'
	            new_component +='<span class="hidden-xs">'+data.navbar_title+'</span>'
			    new_component +='<span class="visible-xs-inline-block action-icon '+data.navbar_icon+'"></span>'
			    new_component +='</a>'
			    new_component +='</li>'
			}
			if(new_component != null){
				original_component.replaceWith($(new_component))
			}
			
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
	if(data.removed && concerned_view){
        data.search_item.remove()
	}
}


function list_channels_component(data){
	if(data.removed && data.channel_item){
        var channel_len = $(data.channel_item.parents('.channels-block').find('.channel-title .channel-len').first())
		var nb = parseInt(channel_len.text().replace('(', '').replace(')', ''))-1
		channel_len.text('('+nb+')')
		data.channel_item.remove()
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


var pseudo_react_components = {
	'support_action': [nav_bar_component, view_title_component, list_items_component],
	'footer_action': [nav_bar_component, footer_action_component,
	                  view_title_component, list_items_component],
	'redirect_action': [redirect_component, list_items_component, view_title_component],
	'dropdown_action': [dropdown_action_component, list_channels_component]
}

function update_components(data){
    var actionid = data.action_id
    var components_to_update = pseudo_react_components[actionid]
    $.each(components_to_update, function(index){
    	this(data)	
    })
}
