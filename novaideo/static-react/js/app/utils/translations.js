/* eslint max-len: "off", quotes: ["error", "double"] */
const Translations = {
  fr: {
    common: {
      termesConditions: "Termes & conditions",
      you: "Vous",
      signIn: "Se connecter",
      singUp: "Créer un compte",
      haveAccount: "Vous avez un compte sur cette plateforme?",
      readAccept: "J'ai lu et j'accepte les ",
      dontHaveAccount: "Vous n'avez pas encore de compte sur cette plateforme ?",
      requestInvitation: "Vous essayez de créer un compte ? Demandez à l’administrateur de la plateforme de vous inviter",
      tryingCreateAccount: "Vous essayez de créer un compte ?",
      createAccount: "Créer un nouveau compte",
      failedLogin: "Désolé, vous avez entré un identifiant ou un mot de passe incorrect.",
      needLogin: "Vous devez être connecté pour effectuer cette action et plus encore. Veuillez vous connecter ou vous inscrire.",
      pinned: "Épinglés",
      moreResult: "Afficher plus de résultats",
      emojis: {
        currentUserTooltip: "Vous (cliquez pour supprimer)",
        currentTooltipTitle: "avez réagi avec %{emoji}",
        tooltipTitle: "ont réagi avec %{emoji}",
        tooltipTitle_1: "a réagi avec %{emoji}"
      },
      clickDownload: "Cliquer pour télécharger",
      remove: "Supprimer",
      examinationClick: "%{name} (Cliquer pour voir l'avis des examinateurs)",
      imageSlider: {
        downLoadImage: "Cliquer pour télécharger",
        downLoadImageSize: "Cliquer pour télécharger (%{size})"
      },
      search: "Rechercher sur la plateforme",
      searchData: "résultats de recherche pour : ",
      searchData_1: "résultat de recherche pour : "
    },
    idea: {
      private: "Privée",
      privatePublishAction: "Privée (Cliquer pour publier)",
      favorable: "Favorable",
      unfavorable: "Défavorable",
      toStudy: "À retravailler"
    },
    editor: {
      addEmbed: "Integrer le contenu d'une URL (une video, un article ....)",
      addImage: "Ajouter une image",
      addSeparator: "Ajouter un séparateur",
      addEmbedForm: "Integrer le contenu d'une URL",
      addEmbedFormPlaceholder: "Entrer une url",
      addEmbedFormSubmission: "Integrer",
      heading1: "Titre 1",
      heading2: "Titre 2",
      heading3: "Titre 3",
      blockquote: "Blockquote",
      unorderedL: "Liste non ordonnée",
      orderedL: "Liste ordonnée",
      todoL: "Liste de choses à faire",
      bold: "Gras",
      italic: "Italioque",
      underline: "Souligné",
      highlight: "Accentué",
      addLink: "Ajouter un lien"
    },
    processes: {
      novaideoabstractprocess: {
        select: {
          title: "Suivre",
          description: "Suivre"
        },
        deselect: {
          title: "Ne plus suivre",
          description: "Retirer de mes suivis"
        },
        addreaction: {
          title: "Ajouter une réaction",
          description: "Ajouter une réaction"
        }
      },
      ideamanagement: {
        create: {
          title: "",
          description: "",
          submission: "Enregistrer"
        },
        createAndPublish: {
          submission: "Enregistrer et publier"
        },
        edit: {
          title: "Editer",
          description: "Editer la proposition",
          submission: "Enregistrer"
        },
        publish: {
          title: "Publier",
          description: "Publier la proposition",
          confirmation: "Voulez-vous vraiment publier cette proposition ? Cette opération est irréversible.",
          submission: "Oui ! Publier"
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
          title: "Commenter la proposition",
          description: "Commenter la proposition"
        }
      },
      commentmanagement: {
        transformtoidea: {
          title: "Transformer en une proposition",
          description: "Transformer en une proposition"
        },
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
          title: "Message",
          description: "Discuter"
        },
        login: {
          title: "Se connecter à %{siteTitle}"
        },
        logout: {
          title: "Se déconnecter de %{siteTitle}"
        },
        edit: {
          title: "Paramètres",
          description: "Paramètres du compte"
        },
        getApiToken: {
          title: "Obtenir un jeton API",
          description: "Obtenir un jeton API"
        },
        editPassword: {
          title: "Changer le mot de passe",
          description: "Paramètres du compte"
        },
        assignRoles: {
          title: "Assigner des rôles",
          description: "Assigner des rôles"
        },
        see: {
          title: "Profil",
          description: "Voir mon profil"
        },
        activate: {
          title: "Activer le compte",
          description: "Activer le compte",
          confirmation:
            "Voulez-vous vraiment activer ce compte utilisateur ? L'utilisateur pourra se connecter à la plateforme et y ajouter du contenu",
          submission: "Oui ! Activer"
        },
        deactivate: {
          title: "Désactiver le compte",
          description: "Désactiver le compte",
          confirmation:
            "Voulez-vous vraiment désactiver ce compte utilisateur ? L'utilisateur ne pourra plus se connecter à la plateforme",
          submission: "Oui ! Désactiver"
        }
      },
      registrationmanagement: {
        registration: {
          title: "Créer un nouveau compte"
        }
      }
    },
    channels: {
      switchChat: "Accéder à mes discussions",
      switchApp: "Accéder à mes contenus",
      jump: "Accéder à...",
      jumpSearch: "Rechercher sur la plateforme",
      channels: "Discussions",
      thread: "Fil de discussion",
      edited: "modifié",
      noMessage: "Aucun message n'est encore posté sur cette discussion ! Soyez le premier à poster un message.",
      ctComment: "Actuellement, la discussion est bloquée et aucun message ne peut être posté.",
      private: "Discussions privées",
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
      },
      unreadMessages: "nouveaux messages",
      unreadMessages_1: "nouveau message",
      noUserCtComment: "Vous ne pouvez pas envoyer des messages à #%{name}. Veuillez vous connecter avant.",
      noUserCtReply: "Vous ne pouvez pas répendre à %{name}. Veuillez vous connecter avant."
    },
    forms: {
      optional: "(facultatif)",
      disableAnonymity: "Désactiver l'anonymat",
      remainAnonymous: "Activer l'anonymat",
      attachFiles: "Attacher des fichiers",
      searchOrAdd: "Recherche ou ajout",
      search: "Recherche",
      cancel: "Annuler",
      add: "Ajouter",
      record: "Enregistrer un message vocal",
      required: "Champs obligatoires",
      idea: {
        title: "Titre de la proposition",
        titleHelper: "Titre",
        textPlaceholder: "J'ai une proposition !",
        textPlaceholderOpened: "Le texte de votre proposition ici",
        keywords: "Ajouter des mots clés",
        addProposal: "Ajouter une nouvelle proposition"
      },
      comment: {
        textPlaceholder: "Envoyer un message à #%{name}",
        searchPlaceholder: "Rechercher dans #%{name}"
      },
      singin: {
        email: "votre-email@exemple.com",
        password: "Mot de passe",
        passwordConfirmation: "Confirmation de mot de passe",
        firstName: "Nom",
        lastName: "Prénom",
        invalidEmail: "adresse e-mail invalide",
        passwordsNotMatch: "Les mots de passe que vous avez entrés ne correspondent pas",
        acceptTerms: "Veuillez accepter les Terms & Conditions",
        emailInUse: "Adresse e-mail déjà utilisée",
        loginNotValid: "L'identifiant n'est pas valide",
        enterLogin: "Saisissez votre <strong>identifiant</strong> et votre <strong>mot de passe</strong>.",
        accountCreated: "Votre compte a été créé",
        confirmationSent:
          "Un e-mail de confirmation a été envoyé à votre compte et devrait apparaître dans votre boîte de réception dans quelques minutes. Il contient un lien de confirmation, veuillez cliquer dessus pour confirmer votre adresse e-mail. Vérifiez votre dossier spam si vous n'avez pas reçu d'e-mail de confirmation."
      },
      editProfile: {
        save: "Enregistrer mes données",
        confirmation: "Vos données de profile ont bien été enregistrées",
        error: "Une erreur est survenue! Les données de votre profil n'ont pas été enregistrées"
      },
      editPassword: {
        save: "Modifier mon mot de passe",
        confirmation: "Votre mot de passe a été modifié",
        error: "Une erreur est survenue! Votre mot de passe n'a pas été modifié. Veuillez vérifier votre mot de passe actuel",
        currentPassword: "Votre mot de passe",
        newPassword: "Le nouveau mot de passe"
      },
      editApiToken: {
        save: "Obtenir un nouveau jeton API",
        confirmation: "Votre nouveau jeton API a été généré",
        error: "Une erreur est survenue! Votre jeton API n'a pas été généré. Veuillez vérifier votre mot de passe actuel",
        password: "Votre mot de passe",
        message: "Votre jeton API:"
      },
      assignRoles: {
        save: "Changer les rôles",
        confirmation: "Les rôles ont été changés",
        error: "Une erreur est survenue! Les rôles n'ont pas été changés",
        roles: "Les rôles"
      }
    },
    evaluation: {
      tokens: "Jetons",
      tokens_1: "Jeton",
      support: "Soutiens",
      support_1: "Soutien",
      opposition: "Oppositions",
      opposition_1: "Opposition"
    },
    examination: {
      examin: "Examens",
      examin_1: "Examen",
      favorable: "Favorable",
      unfavorable: "Défavorable",
      toStudy: "À retravailler"
    },
    date: {
      format: "D MMMM YYYY",
      format2: "DD-MM-YYYY",
      format3: "D MMMM YYYY à h [h] mm [min] ss [s]",
      format4: "D MMMM YYYY à h [h] mm [min]",
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
      myEvaluations: "Mes appréciations",
      folloers: "Suivis par %{count} personnes",
      folloers_1: "Suivis par une personne",
      folloers_0: "N'est suivis par personne",
      search: "Rechercher dans les contenus de %{name}",
      subscribed: "Inscrit le %{date}",
      noUserCard: "Connecter vous pour accéder aux données de votre profil et plus encore!",
      noUserContents: "Pour accéder à vos contenus vous devez être connecté.",
      noUserChannels: "Pour accéder à vos discussion vous devez être connecté.",
      confirmRegistration: "Veuillez patienter pendant que nous vérifions votre inscription !"
    },
    roles: {
      Member: "Membre",
      Admin: "Administrateur",
      SiteAdmin: "Administrateur du site",
      Moderator: "Moderateur",
      Examiner: "Examinateur"
    }
  },
  en: {
    common: {
      termesConditions: "Termes & conditions",
      you: "You",
      signIn: "Sign in",
      singUp: "Sing up",
      haveAccount: "You have an account on this platform?",
      readAccept: "I have read and I accept the ",
      dontHaveAccount: "Don't have an account on this platform yet?",
      requestInvitation: "Trying to create a account? Contact the platform administrator for an invitation",
      tryingCreateAccount: "Trying to create an account?",
      createAccount: "Create a new account",
      failedLogin: "Sorry, you entered an incorrect identifier or password.",
      needLogin: "You must be logged in to perform this action and more. Please sign in or register",
      pinned: "Pinned",
      moreResult: "See more results",
      emojis: {
        currentUserTooltip: "You (click to remove)",
        currentTooltipTitle: "reacted with %{emoji}",
        tooltipTitle: "reacted with %{emoji}",
        tooltipTitle_1: "reacted with %{emoji}"
      },
      clickDownload: "Click to download",
      remove: "Remove",
      examinationClick: "%{name} (Click to see the reviewers' opinion)",
      imageSlider: {
        downLoadImage: "Click to download",
        downLoadImageSize: "Click to download (%{size})"
      },
      search: "Search on the platform",
      searchData: "search results for: ",
      searchData_1: "search result for : "
    },
    idea: {
      private: "Private",
      privatePublishAction: "Private (Click to publish)",
      favorable: "Positive",
      unfavorable: "Negative",
      toStudy: "To be re-worked upon"
    },
    editor: {
      addEmbed: "Embed the content of an URL (a video, an article ....)",
      addImage: "Add an image",
      addSeparator: "Add a separator",
      addEmbedForm: "Embed the content of an URL",
      addEmbedFormPlaceholder: "Enter an URL",
      addEmbedFormSubmission: "Embed",
      heading1: "Heading 1",
      heading2: "Heading 2",
      heading3: "Heading 3",
      blockquote: "Blockquote",
      unorderedL: "Unordered list",
      orderedL: "Ordered list",
      todoL: "To do list",
      bold: "Bold",
      italic: "Italic",
      underline: "Underline",
      highlight: "Highlight selection",
      addLink: "Add a link"
    },
    processes: {
      novaideoabstractprocess: {
        select: {
          title: "Follow",
          description: "Follow"
        },
        deselect: {
          title: "Unfollow",
          description: "Unfollow"
        },
        addreaction: {
          title: "Ass a reaction",
          description: "Ass a reaction"
        }
      },
      ideamanagement: {
        create: {
          title: "",
          description: "",
          submission: "Save"
        },
        createAndPublish: {
          submission: "Save and publish"
        },
        edit: {
          title: "Edit",
          description: "Edit the proposal",
          submission: "Save"
        },
        publish: {
          title: "Publish",
          description: "Publish the proposal",
          confirmation: "Are you sure you want to publish this proposal? This cannot be undone.",
          submission: "Yes ! Publish"
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
          title: "Comment the proposal",
          description: "Comment the proposal"
        }
      },
      commentmanagement: {
        transformtoidea: {
          title: "Transform to a proposal",
          description: "Transform to a proposal"
        },
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
          title: "Discuss",
          description: "Discuss"
        },
        login: {
          title: "Sign in to %{siteTitle}"
        },
        logout: {
          title: "Sign out from %{siteTitle}"
        },
        edit: {
          title: "Paramters",
          description: "Paramters of the account"
        },
        getApiToken: {
          title: "Obtenir un jeton API",
          description: "Obtenir un jeton API"
        },
        editPassword: {
          title: "Changer le mot de passe",
          description: "Paramètres du compte"
        },
        assignRoles: {
          title: "Assigner des rôles",
          description: "Assigner des rôles"
        },
        see: {
          title: "Profile",
          description: "Profile"
        },
        activate: {
          title: "Activate the account",
          description: "Activate the account",
          confirmation:
            "Are you sure you want t activate this user account? The user will be able to connect to the platform and add content",
          submission: "Yes! Activate"
        },
        deactivate: {
          title: "Deactivate the account",
          description: "Deactivate the account",
          confirmation:
            "Are you sure you want to deactivate this user account? The user will not be able to login to the platform anymore",
          submission: "Yes! Disable"
        }
      },
      registrationmanagement: {
        registration: {
          title: "Create a new account"
        }
      }
    },

    channels: {
      switchChat: "Access my discussions",
      switchApp: "Access my contents",
      jump: "Jump to...",
      jumpSearch: "Search on the platform",
      channels: "Discussions",
      thread: "Thread",
      edited: "edited",
      noMessage: "There are no messages on this discussion yet! Be the first to post a message.",
      ctComment: "Currently, the discussion is blocked and no message can be posted.",
      private: "Private discussions",
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
      },
      unreadMessages: "new messages",
      unreadMessages_1: "new message",
      noUserCtComment: "You cannot send a message to #%{name}. Please login before.",
      noUserCtReply: "You cannot answer %{name}. Please login before."
    },
    forms: {
      optional: "(optional)",
      disableAnonymity: "Disable anonymity",
      remainAnonymous: "Remain anonymous",
      attachFiles: "Attach files",
      searchOrAdd: "Search or add",
      search: "Search",
      cancel: "Cancel",
      add: "Add",
      record: "Record a voice message",
      required: "Required",
      idea: {
        title: "The title of the proposal",
        titleHelper: "Title",
        textPlaceholder: "I have an proposal!",
        textPlaceholderOpened: "The text of your proposal here",
        keywords: "Add keywords",
        addProposal: "Add a new proposal"
      },
      comment: {
        textPlaceholder: "Submit a message to #%{name}",
        searchPlaceholder: "Search in #%{name}"
      },
      singin: {
        email: "yor-email@example.com",
        password: "Password",
        passwordConfirmation: "Password (confirm)",
        firstName: "First name",
        lastName: "last name",
        invalidEmail: "Invalid email address",
        passwordsNotMatch: "The passwords that you have entered do not match",
        acceptTerms: "Please accept the Terms & Conditions",
        emailInUse: "Email address already in use",
        loginNotValid: "The login is not valid",
        enterLogin: "Enter your <strong>identifier</strong> and <strong>password</strong>.",
        accountCreated: "Your account has been created",
        confirmationSent:
          "A confirmation e-mail has been sent to your account and should be in your inbox in a few minutes. It contains a confirmation link, please click on it in order to confirm your e-mail address. Check your spam folder if you did not receive a confirmation e-mail."
      },
      editProfile: {
        save: "Save my data",
        confirmation: "Your profile data has been saved",
        error: "An error has occurred! Your profile data has not been saved"
      },
      editPassword: {
        save: "Edit my password",
        confirmation: "Your password has been edited",
        error: "An error has occurred! Your password has not been edited. Please check your current password",
        currentPassword: "Your password",
        newPassword: "The new password"
      },
      editApiToken: {
        save: "Obtenir un nouveau jeton API",
        confirmation: "Votre nouveau jeton API a été généré",
        error: "Une erreur est survenue! Votre jeton API n'a pas été généré. Veuillez vérifier votre mot de passe actuel",
        password: "Votre mot de passe",
        message: "Your API token:"
      },
      assignRoles: {
        save: "Change the roles",
        confirmation: "The roles has been changed",
        error: "An error has occurred! The roles has not been changed",
        roles: "The roles"
      }
    },
    evaluation: {
      tokens: "Tokens",
      tokens_1: "Token",
      support: "Supports",
      support_1: "Support",
      opposition: "Oppositions",
      opposition_1: "Opposition"
    },
    examination: {
      examin: "Examinations",
      examin_1: "Examination",
      favorable: "Positive",
      unfavorable: "Negative",
      toStudy: "To be re-worked upon"
    },
    date: {
      format: "MMMM Do, YYYY",
      format2: "YYYY-MM-DD",
      format3: "MMMM Do, YYYY at h [h] mm [min] ss [s]",
      format4: "MMMM Do, YYYY at h [h] mm [min]",
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
      myEvaluations: "My evaluations",
      folloers: "Followed by %{count} members",
      folloers_1: "Followed by one member",
      folloers_0: "Not followed",
      search: "Search on the %{name} contents",
      subscribed: "Subscribed the %{date}",
      noUserCard: "Connecter vous pour accéder aux données de votre profil et plus encore!",
      noUserContents: "Pour accéder à vos contenus vous devez être connecté.",
      noUserChannels: "Pour accéder à vos discussion vous devez être connecté.",
      confirmRegistration: "Please wait while we check your registration!"
    },
    roles: {
      Member: "Member",
      Admin: "Administrator",
      SiteAdmin: "Site administrator",
      Moderator: "Moderator",
      Examiner: "Examiner"
    }
  }
};

module.exports = Translations; // keep commonJS syntax for the node i18n:export script to work