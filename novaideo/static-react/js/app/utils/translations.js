/* eslint max-len: "off", quotes: ["error", "double"] */
const Translations = {
  fr: {
    forms: {
      optional: "(facultatif)",
      disableAnonymity: "Désactiver l'anonymat",
      remainAnonymous: "Activer l'anonymat",
      attachFiles: "Attacher des fichiers",
      searchOrAdd: "Recherche ou ajout",
      search: "Recherche",
      createIdea: {
        title: "Titre de l'idée",
        titleHelper: "Ajouter un titre à votre idée",
        textPlaceholder: "J'ai une idée !",
        textPlaceholderOpened: "Le texte de votre idée ici",
        keywords: "Ajouter des mots clés"
      },
      comment: {
        textPlaceholder: "Envoyer un message à #%{name}"
      }
    },
    evaluation: {
      tokens: "Jetons",
      support: "Soutiens",
      opposition: "Oppositions",
      supportTheIdea: "Soutenir l'idée",
      opposeTheIdea: "S'opposer à l'idée",
      withdrawTokenIdea: "Retirer mon jeton"
    },
    date: {
      format: "D MMMM YYYY",
      format2: "DD-MM-YYYY",
      format3: "D MMMM YYYY à h [h] mm [min] ss [s]",
      today: "Aujourd'hui",
      yesterday: "Hier",
      todayFormat: "[Aujourd'hui] à h [h] mm [min] ss [s]",
      yesterdayFormat: "[Hier à] h [h] mm [min] ss [s]"
    },
    time: {
      format: "h [h] mm"
    }
  },
  en: {
    forms: {
      optional: "(optional)",
      disableAnonymity: "Disable anonymity",
      remainAnonymous: "Remain anonymous",
      attachFiles: "Attach files",
      searchOrAdd: "Search or add",
      search: "Search",
      createIdea: {
        title: "The title of the idea",
        titleHelper: "Add a title to your idea",
        textPlaceholder: "I have an idea!",
        textPlaceholderOpened: "The text of your idea here",
        keywords: "Add keywords"
      },
      comment: {
        textPlaceholder: "Submit a message to #%{name}"
      }
    },
    evaluation: {
      tokens: "Tokens",
      support: "Supports",
      opposition: "Oppositions",
      supportTheIdea: "Support the idea",
      opposeTheIdea: "Oppose the idea",
      withdrawTokenIdea: "Withdraw my token"
    },
    date: {
      format: "MMMM Do, YYYY",
      format2: "YYYY-MM-DD",
      format3: "MMMM Do, YYYY at h [h] mm [min] ss [s]",
      today: "Today",
      yesterday: "Yesterday",
      todayFormat: "[Today at] h [h] mm [min] ss [s]",
      yesterdayFormat: "[Yesterday at] h [h] mm [min] ss [s]"
    },
    time: {
      format: "h \\h mm"
    }
  }
};

module.exports = Translations; // keep commonJS syntax for the node i18n:export script to work