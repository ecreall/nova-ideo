function reset_cookie(){
  var $this = $(this);
  if ($this.hasClass('admin-in')){
     $.cookie('admin_nav', 'off', {path: '/',  expires: 1});
     var span = $($this.find('span').first())
     span.removeClass('glyphicon-chevron-up')
     span.addClass('glyphicon-chevron-down');
     $this.removeClass('admin-in')
  }else{
    $.cookie('admin_nav', 'on', {path: '/',  expires: 1});
     var span = $($this.find('span').first())
     span.addClass('glyphicon-chevron-up')
     span.removeClass('glyphicon-chevron-down')
     $this.addClass('admin-in')
  }
}

$(document).ready(function(){
      $('.btn.admin-nav-bar-toggle').on('click', reset_cookie);
      $('.admin-nav .group').hover(
        function(){
            var actions = $($(this).find('ul.actions').first());
            actions.show();},
        function(){
            var actions = $($(this).find('ul.actions').first());
            actions.hide();
        });
});
