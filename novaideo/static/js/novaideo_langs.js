novaideoI18n = {
'en': {
  'Or': 'Or',
  'Period expired': 'Period expired',
  ' caracteres maximum)': ' caracteres maximum)',
  ' remaining characters': ' remaining characters'
},

'fr':{
 'Or': 'Ou',
 'Period expired': 'Durée expirée',
  ' caracteres maximum)': ' caractères maximum)',
  ' remaining characters': ' caractères restants'
}
}

//TODO add Translation class see tinymce langs...
function novaideo_translate(msgid){
      var local = novaideo_get_language()
      var msgs = novaideoI18n[local]
      if (msgid in msgs){
         return msgs[msgid]  
      }

      return msgid
}
