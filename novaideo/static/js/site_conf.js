
$(
  document
).on(
  "click",
  ".conf-form-anonymisation input[type='checkbox'][name='anonymisation']",
  function(event) {
    if ($(this).is(":checked")) {
      $(".conf-form-anonymisation-kind").slideDown("hide-bloc")
    }else{
      $(".conf-form-anonymisation-kind").slideUp("hide-bloc")
    }
  }
)


$(document).ready(function() {
  if ($(".conf-form-anonymisation input[type='checkbox'][name='anonymisation']").is(":checked")) {
      $(".conf-form-anonymisation-kind").slideDown("hide-bloc")
  }else{
    $(".conf-form-anonymisation-kind").slideUp("hide-bloc")
  }
})
