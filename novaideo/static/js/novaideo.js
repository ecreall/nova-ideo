$(document).ready(function(){
  $("[name='globalmenuswitch']").bootstrapSwitch();

  $("[name='globalmenuswitch']").on('switchChange.bootstrapSwitch',function() {
     $('#navbaruser').slideToggle();
  });

  $('nav a nav-control').on('click', function(){
      $(".navbar-toggle").click();
  });

  $('.panel-collapse').on('hide.bs.collapse', function () {
    $(this).siblings().find('a span').attr('class', 'glyphicon glyphicon-plus');
  });

  $('.panel-collapse').on('show.bs.collapse', function () {
    $(this).siblings().find('a span').attr('class', 'glyphicon glyphicon-minus');
  });
  $('#results').infinitescroll({
    navSelector  : "#results .batch",
                   // selector for the paged navigation (it will be hidden)
    nextSelector : "#results .pager .next",
                   // selector for the NEXT link (to page 2)
    itemSelector : "#results div.col-md-12",
                   // selector for all items you'll retrieve
    pathParse: function(path, next_page) {
       var parts = path.match(/^(.*?batch_num=)1(.*|$)/).slice(1);
// ["http://0.0.0.0:6543/@@seemyideas?batch_num=", "&batch_size=1&action_uid=-4657697968224339750"]
// substanced Batch starts at 0, not 1
       var f = function(currPage) {
         return parts.join(currPage - 1);
       };
       return f;
    },
    loading: {
      finishedMsg: "<em>No more item.</em>"
    }
  });
});

