novaideoI18n = {
'en': {
  'Or': 'Or',
  'Period expired': 'Period expired'
},

'fr':{
 'Or': 'Ou',
 'Period expired': 'Durée expirée'
}
}

//TODO add Translation class see tinymce langs...
function novaideo_translate(msgid){
      var local = get_language()
      var msgs = novaideoI18n[local]
      if (msgid in msgs){
         return msgs[msgid]  
      }

      return msgid
}
