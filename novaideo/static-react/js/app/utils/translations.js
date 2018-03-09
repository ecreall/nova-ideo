/* eslint max-len: "off", quotes: ["error", "double"] */
const Translations = {
  fr: {
    common: {
      pinned: "Épinglés",
      moreResult: "Afficher plus de résultats",
      emojis: {
        currentUserTooltip: "Vous (cliquez pour supprimer)",
        currentTooltipTitle: "avez réagi avec %{emoji}",
        tooltipTitle: "ont réagi avec %{emoji}",
        tooltipTitle_1: "a réagi avec %{emoji}"
      },
      clickDownload: "Cliquer pour télécharger"
    },
    processes: {
      novaideoabstractprocess: {
        select: {
          title: "Suivre"
        },
        deselect: {
          title: "Retirer de mes suivis"
        },
        addreaction: {
          title: "Ajouter une réaction"
        }
      },
      ideamanagement: {
        create: {
          title: "",
          description: ""
        },
        delete: {
          title: "Supprimer",
          description: "Supprimer la proposition",
          confirmation: "Voulez-vous vraiment supprimer cette proposition ? Cette opération est irréversible.",
          submission: "Oui ! Supprimer"
        },
        oppose: {
          title: "S'opposer",
          description: "S'opposer à la proposition"
        },
        support: {
          title: "Soutenir",
          description: "Soutenir la proposition"
        },
        withdrawToken: {
          title: "Retirer",
          description: "Retirer mon jeton"
        },
        comment: {
          title: "Commenter la proposition"
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
        },
        respond: {
          title: "Répondre",
          description: "Répondre à ce message"
        },
        edit: {
          title: "Éditer",
          description: "Éditer le message",
          submission: "Enregistrer les changements"
        }
      },
      usermanagement: {
        discuss: {
          title: "Discuter"
        }
      }
    },
    channels: {
      switchChat: "Accéder à mes discussions",
      switchApp: "Accéder à mes contenus",
      jump: "Accéder à...",
      channels: "Chaînes",
      thread: "Fil de discussion",
      edited: "modifié",
      noMessage: "Aucun message n'est encore posté sur cette discussion ! Soyez le premier à poster un message.",
      ctComment: "Actuellement, la discussion est bloquée et aucun message ne peut être posté.",
      private: "Messages directs",
      pinnedBlockTitle: "%{count} messages épinglés",
      pinnedBlockTitle_0: "Aucun message épinglé",
      pinnedBlockTitle_1: "Un message épinglé",
      noPinnedBlock:
        "Il n'y a pas encore de messages épinglés ! Ouvrez le menu contextuel des messages importants et choisissez Épingler pour les conserver ici.",
      infoBlockTitle: "Informations sur la chaîne",
      filesBlockTitle: "Fichiers partagés",
      filesBlockTitle_0: "Aucun fichier partagé",
      noFilesBlock: "Il n'y a pas encore de messages avec des fichiers attachées !",
      membersBlockTitle: "%{count} membres",
      membersBlockTitle_0: "Aucun membre",
      membersBlockTitle_1: "Un membre",
      rightTitleAbout: "À propos de la discussion #%{name}",
      searchBlockTitle: "Résultats de la recherche",
      noResultBlock: "Aucun résultat trouvé pour votre recherche ! Vérifiez l'orthographe ou essayez avec un autre terme.",
      usersCommentsFooter:
        "Vous êtes au tout début de votre discussion. Dans cette discussion vous pouvez discuter en privée avec %{name}, partagez des fichiers ou des liens...",
      ideasCommentsFooter:
        "Vous êtes au tout début de cette discussion. Dans cette discussion vous pouvez partager votre point de vu avec les autres utilisateurs, partagez des fichiers ou des liens...",
      ideasCommentsFooterTitle: "Ceci est l'espace de discussion associée à la proposition %{name}.",
      usersCommentsFooterTitle: "Ceci est votre espace de discussion privée avec %{name}.",
      replyCommentFooter:
        "Vous êtes au tout début de ce fil de discussion. Dans ce fil vous pouvez répondre à l'auteur de ce message, partager votre point de vu avec les autres utilisateurs, partagez des fichiers ou des liens...",
      reply: "Ajouter une réponse à %{name}",
      replies: "%{count} réponses",
      replies_1: "Une réponse",
      unreadReplies: "%{count} non lus",
      unreadReplies_1: "Un non lu",
      navbar: {
        info: "Informations sur la discussion",
        pinned: "Les messages épinglés",
        members: "Les membres abonnés à la discussion",
        files: "Les messages avec des fichiers attachés"
      }
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
        title: "Titre de la proposition",
        titleHelper: "Ajouter un titre à votre proposition",
        textPlaceholder: "J'ai une proposition !",
        textPlaceholderOpened: "Le texte de votre proposition ici",
        keywords: "Ajouter des mots clés"
      },
      comment: {
        textPlaceholder: "Envoyer un message à #%{name}",
        searchPlaceholder: "Rechercher dans #%{name}"
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
      pinned: "Pinned",
      moreResult: "See more results",
      emojis: {
        currentUserTooltip: "You (click to remove)",
        currentTooltipTitle: "reacted with %{emoji}",
        tooltipTitle: "reacted with %{emoji}",
        tooltipTitle_1: "reacted with %{emoji}"
      },
      clickDownload: "Click to download"
    },
    processes: {
      novaideoabstractprocess: {
        select: {
          title: "Follow"
        },
        deselect: {
          title: "Unfollow"
        },
        addreaction: {
          title: "Ass a reaction"
        }
      },
      ideamanagement: {
        create: {
          title: "",
          description: ""
        },
        delete: {
          title: "Remove",
          description: "Remove the proposal",
          confirmation: "Are you sure you want to delete this proposal? This cannot be undone.",
          submission: "Yes ! Remove"
        },
        oppose: {
          title: "Oppose",
          description: "Oppose the proposal"
        },
        support: {
          title: "Support",
          description: "Support the proposal"
        },
        withdrawToken: {
          title: "Withdraw",
          description: "Withdraw my token"
        },
        comment: {
          title: "Comment the proposal"
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
        },
        respond: {
          title: "Respond",
          description: "Respond to this message"
        },
        edit: {
          title: "Edit",
          description: "Edit this message",
          submission: "Save Changes"
        }
      },
      usermanagement: {
        discuss: {
          title: "Discuss"
        }
      }
    },

    channels: {
      switchChat: "Access my discussions",
      switchApp: "Access my contents",
      jump: "Jump to...",
      channels: "Channels",
      thread: "Thread",
      edited: "edited",
      noMessage: "There are no messages on this discussion yet! Be the first to post a message.",
      ctComment: "Currently, the discussion is blocked and no message can be posted.",
      private: "Direct messages",
      pinnedBlockTitle: "%{count} pinned messages",
      pinnedBlockTitle_0: "No pinned messages",
      pinnedBlockTitle_1: "One pinned message",
      noPinnedBlock:
        "No messages have been pinned yet! Open the context menu on important messages and choose Pin to stick them here.",
      infoBlockTitle: "Channel information",
      filesBlockTitle: "Shared files",
      filesBlockTitle_0: "No shared files",
      noFilesBlock: "There are no messages with attached files yet!",
      membersBlockTitle: "%{count} members",
      membersBlockTitle_0: "No members",
      membersBlockTitle_1: "One member",
      rightTitleAbout: "About the discussion #%{name}",
      searchBlockTitle: "Search results",
      noResultBlock: "No results found for your search ! Check your spelling or try another term",
      usersCommentsFooter:
        "You are at the beginning of your discussion, in this discussion you can discuss privately with %{name}, share files or links ...",
      ideasCommentsFooter:
        "You are at the beginning of this discussion.In this discussion you can share your point of view with other users, share files or links ...",
      ideasCommentsFooterTitle: "This is the discussion space associated with the proposal %{name}.",
      usersCommentsFooterTitle: "This is your private discussion with %{name}.",
      replyCommentFooter:
        "You are at the beginning of this thread. In this thread you can respond to the author of this message, share your point of view with other users, share files or links ...",
      reply: "Add reply to %{name}",
      replies: "%{count} replies",
      replies_1: "One reply",
      unreadReplies: "%{count} unread",
      unreadReplies_1: "One unread",
      navbar: {
        info: "Channel information",
        pinned: "Pinned messages",
        members: "Members",
        files: "Files"
      }
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
        title: "The title of the proposal",
        titleHelper: "Add a title to your proposal",
        textPlaceholder: "I have an proposal!",
        textPlaceholderOpened: "The text of your proposal here",
        keywords: "Add keywords"
      },
      comment: {
        textPlaceholder: "Submit a message to #%{name}",
        searchPlaceholder: "Search in #%{name}"
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