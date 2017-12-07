$(document).on("click", ".emoji-input-container .emoji-inner" ,function(event) {
   var $this = $(this)
   var emoji = $this.data('actual')
   var input = $this.parents(".emoji-input-container").find('input').first()
   var current_value = input.val()
   if (emoji === current_value) {
    input.val('')
   } else {
    input.val(emoji)
   }
   $this.parents('form').first().find('button[type="submit"]').first().click()
})