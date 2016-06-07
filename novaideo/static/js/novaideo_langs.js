
novaideoI18n = {
'en': {
  'Or': 'Or',
  'Period expired': 'Period expired',
  ' caracteres maximum)': ' caracteres maximum)',
  ' remaining characters': ' remaining characters',
  'There was a problem with your submission.': 'There was a problem with your submission.',
  "The title is required!": "The title is required" ,
  "The abstract is required!": "The text is required" ,
  "Keywords are required!": "Keywords are required" ,
  "The idea is not added!": "The idea is not added", 
  "Comment sent": "Comment sent" ,
  "Your comment is integrated": "Your comment is integrated", 
  "Idea already exist!": "Idea already exist" ,
  "Please select a valid idea!": "Please select a valid idea",
  "No more item.": "No more item.",
  "Message sent": "Message sent",
  "Your message has been delivered to the following recipients": "Your message has been delivered to the following recipients"
},

'fr':{
  'Or': 'Ou',
  'Period expired': 'Durée expirée',
  ' caracteres maximum)': ' caractères maximum)',
  ' remaining characters': ' caractères restants',
  'There was a problem with your submission.': 'Un problème a été rencontré lors de votre soumission. Merci de vérifier les informations saisies.',
  "The title is required!": "Le titre est requis" ,
  "The abstract is required!": "Le texte est requis" ,
  "Keywords are required!": "Les mots clés sont requis" ,
  "The idea is not added!": "L'idée n'est pas ajoutée", 
  "Comment sent": "Votre message est bien envoyé" ,
  "Your comment is integrated": "Votre message est prise en compte", 
  "Idea already exist!": "Idée est déjà incluse" ,
  "Please select a valid idea!": "Veuillez sélectionner une idée valide",
  "No more item.": "Pas d'autres éléments.",
  "Message sent": "Message envoyé",
  "Your message has been delivered to the following recipients": "Votre message a été envoyé aux destinataires suivants"
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
