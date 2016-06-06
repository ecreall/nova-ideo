function adapt_contact_phone(element){
      var surtax_input = $($($(element).parents('.contact-well').first()).find("input[name='surtax']").first());
      var formgroup = surtax_input.parents('.form-group').first();
      formgroup.css({'margin-left': '20px', 'margin-top': '-10px', 'font-size': '12px', 'color': 'gray'});
      if ($(element).val() != ''){
         if (formgroup.hasClass('hide-bloc')) {
            formgroup.removeClass('hide-bloc');
         };
      }else{
         if (!formgroup.hasClass('hide-bloc')) {
            formgroup.addClass('hide-bloc');
         };
      };
};


function init_contact_phone(elements){
   elements.keyup(function(){
        adapt_contact_phone(this)
   });

   for (i=0; i<elements.length; i++){
         var element = elements[i];
         adapt_contact_phone(element)
   };

};

$(document).ready(function(){

   init_contact_phone($('.contact-phone'));

   $('form').on('item_added', function(event){
         var item_added = $(event.element);
         init_contact_phone($(item_added.find('.contact-phone')));
      });

});
