/* eslint max-len: "off", quotes: ["error", "double"] */
const Translations = {
  fr: {
    common: {
      pinned: "Épinglés"
    },
    processes: {
      ideamanagement: {
        create: {
          title: "",
          description: ""
        },
        delete: {
          title: "Supprimer",
          description: "Supprimer l'idée",
          confirmation: "Voulez-vous vraiment supprimer cette idée ? Cette opération est irréversible.",
          submission: "Oui ! Supprimer"
        },
        oppose: {
          title: "S'opposer",
          description: "S'opposer à l'idée"
        },
        support: {
          title: "Soutenir",
          description: "Soutenir l'idée"
        },
        withdrawToken: {
          title: "Retirer",
          description: "Retirer mon jeton"
        }
      },
      commentmanagement: {
        delete: {
          title: "Supprimer",
          description: "Supprimer le message",
          confirmation: "Voulez-vous vraiment supprimer ce message de cette conversation ? Cette opération est irréversible.",
          submission: "Oui ! Supprimer"
        },
        pin: {
          title: "Épingler",
          description: "Épingler le message",
          confirmation: "Voulez-vous vraiment épingler ce message à cette conversation ?",
          submission: "Oui ! Épingler"
        },
        unpin: {
          title: "Désépingler",
          description: "Désépingler le message",
          confirmation: "Voulez-vous vraiment désépingler ce message de cette conversation ?",
          submission: "Oui ! Désépingler"
        }
      }
    },
    channels: {
      jump: "Accéder à...",
      channels: "Chaînes",
      private: "Messages directs",
      pinnedBlockTitle: "Messages épinglés",
      infoBlockTitle: "Informations sur la chaîne",
      filesBlockTitle: "Fichiers partagés",
      membersBlockTitle: "%{total} membres",
      rightTitleAbout: "À propos de la discussion #%{name}"
    },
    forms: {
      optional: "(facultatif)",
      disableAnonymity: "Désactiver l'anonymat",
      remainAnonymous: "Activer l'anonymat",
      attachFiles: "Attacher des fichiers",
      searchOrAdd: "Recherche ou ajout",
      search: "Recherche",
      cancel: "Annuler",
      idea: {
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
      opposition: "Oppositions"
    },
    date: {
      format: "D MMMM YYYY",
      format2: "DD-MM-YYYY",
      format3: "D MMMM YYYY à h [h] mm [min] ss [s]",
      today: "[Aujourd'hui]",
      yesterday: "[Hier]",
      todayFormat: "[Aujourd'hui] à h [h] mm [min] ss [s]",
      yesterdayFormat: "[Hier à] h [h] mm [min] ss [s]"
    },
    time: {
      format: "h [h] mm"
    },
    user: {
      myContents: "Mes contenus",
      myFollowings: "Mes suivis",
      myEvaluations: "Mes appréciations"
    }
  },
  en: {
    common: {
      pinned: "Pinned"
    },
    processes: {
      ideamanagement: {
        create: {
          title: "",
          description: ""
        },
        delete: {
          title: "Remove",
          description: "Remove the idea",
          confirmation: "Are you sure you want to delete this idea? This cannot be undone.",
          submission: "Yes ! Remove"
        },
        oppose: {
          title: "Oppose",
          description: "Oppose the idea"
        },
        support: {
          title: "Support",
          description: "Support the idea"
        },
        withdrawToken: {
          title: "Withdraw",
          description: "Withdraw my token"
        }
      },
      commentmanagement: {
        delete: {
          title: "Remove",
          description: "Remove the message",
          confirmation: "Are you sure you want to delete this message from this conversation? This cannot be undone.",
          submission: "Yes ! Remove"
        },
        pin: {
          title: "Pin",
          description: "Pin the message",
          confirmation: "Are you sure you want to pin this message to this conversation?",
          submission: "Yes ! Pin"
        },
        unpin: {
          title: "Unpin",
          description: "Unpin the message",
          confirmation: "Are you sure you want to unpin this message from this conversation?",
          submission: "Yes ! Unpin"
        }
      }
    },

    channels: {
      jump: "Jump to...",
      channels: "Channels",
      private: "Direct messages",
      pinnedBlockTitle: "Pinned messages",
      infoBlockTitle: "Channel information",
      filesBlockTitle: "Shared files",
      membersBlockTitle: "%{total} members",
      rightTitleAbout: "About the discussion #%{name}"
    },
    forms: {
      optional: "(optional)",
      disableAnonymity: "Disable anonymity",
      remainAnonymous: "Remain anonymous",
      attachFiles: "Attach files",
      searchOrAdd: "Search or add",
      search: "Search",
      cancel: "Cancel",
      idea: {
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
      opposition: "Oppositions"
    },
    date: {
      format: "MMMM Do, YYYY",
      format2: "YYYY-MM-DD",
      format3: "MMMM Do, YYYY at h [h] mm [min] ss [s]",
      today: "[Today]",
      yesterday: "[Yesterday]",
      todayFormat: "[Today at] h [h] mm [min] ss [s]",
      yesterdayFormat: "[Yesterday at] h [h] mm [min] ss [s]"
    },
    time: {
      format: "h \\h mm"
    },
    user: {
      myContents: "My contents",
      myFollowings: "My followings",
      myEvaluations: "My evaluations"
    }
  }
};

module.exports = Translations; // keep commonJS syntax for the node i18n:export script to work