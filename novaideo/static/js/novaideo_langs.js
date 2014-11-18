novaideoI18n = {
'en': {
  'Or': 'Or'
},

'fr':{
 'Or': 'Ou'
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
