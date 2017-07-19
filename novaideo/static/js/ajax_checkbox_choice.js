
$(document).on('click', '.checkbox-scroll .btn-more-scroll.active', function(){
  var $this = $(this)
  var result_scroll = $($this.parents('.checkbox-scroll').first())
  var icon = $(result_scroll.find('.more-icon').first())
  var current_content = result_scroll.find('.result-container').first()
  var url = current_content.data('url')
  var page = current_content.data('page')
  var limit = current_content.data('limit')
  icon.removeClass('glyphicon-option-horizontal')
  $this.removeClass('active')
  icon.addClass('ion-refreshing')
  $.post(url,{'limit': limit, 'page': page}, function(data) {
      var scroll_items_container = $(current_content.find('.scroll-items-container').first())
      if(data && data.total_count>0){
        current_content.data('page', data.next_page)
        var items = data.items.map(function(item, index){
              return  '<div class="scroll-item checkbox '+(item.imported ? 'imported' : '')+'">'+
                        '<label for="'+item.id+'">'+
                          '<input type="checkbox"  name="checkbox" value="'+item.id+'" id="'+item.id+'"'+
                           (item.imported ? 'checked="true"': '')+'"/>'+
                          item.text +
                        '</label>'+
                      '</div>'
        })
        scroll_items_container.append(items)
        icon.addClass('glyphicon-option-horizontal')
        $this.addClass('active')
        icon.removeClass('ion-refreshing')
        if(!data.has_next){
           result_scroll.find('.btn-more-scroll').parents('.btn-more-scroll-container').remove()
        }
      }
  })
})