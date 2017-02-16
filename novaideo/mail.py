# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from novaideo import _

""" The contents of e-mails"""

PORTAL_SIGNATURE = """Cordialement,
                                                                                
La Plateforme {novaideo_title}
"""

PORTAL_PRESENTATION = u"""{novaideo_title} est une plateforme participative qui permet à tout membre d'initier des idées pouvant être utilisées dans des propositions améliorées par des groupes de travail. Une fois améliorées, ces propositions peuvent être soumises à l'appréciation des membres et faire l'objet d'une décision d'un comité d'examen.

"""

FIRST_INVITATION_SUBJECT = u"""Invitation à rejoindre la plateforme participative {novaideo_title}"""

FIRST_INVITATION_MESSAGE = u"""
Bonjour,

Nous vous remercions de l'intérêt que vous portez à Nova-Ideo.

{recipient_first_name} vous êtes invité à rejoindre la plateforme participative Nova-Ideo en tant que administrateur du site.

Pour valider votre invitation, vous devez cliquer sur le lien {invitation_url} et suivre les instructions.

Nous vous rappellons que Nova-Ideo est une solution d'innovation participative en ligne qui permet de répondre aux problèmes suivants :
- Vous souhaitez mettre en place une solution d'innovation participative ;
- Vous avez déjà une boite à idées, mais soit elle est vide, soit si pleine qu'il est impossible de trouver les bonnes idées ;
- Vous n'avez pas de temps à passer à gérer les idées et manquez ainsi de nombreuses opportunités, et créez de la déception chez ceux qui ont des idées.

Nova-Ideo permet de recueillir les idées d'un collectif, de trouver les bonnes idées et de les transformer en propositions applicables reflétant tous les points de vue.

Pour cela Nova-Ideo utilise le crowdsourcing en faisant travailler la "foule" sur la transformation des idées en propositions.

Nova-Ideo fusionne le meilleur de la boite à idées, du portail collaboratif et des outils de communication internes et propose des solutions d'innovation sociale à la pointe comme l'utilisation du jugement majoritaire ou l'organisation de la rareté des soutiens/rejets.

Consultez notre page https://www.nova-ideo.com et notamment sa page Documentation https://www.nova-ideo.com/documentation

Suivez notre compte twitter : https://twitter.com/NovaIdeo

Vous pouvez consulter notre présentation détaillée de Nova-Ideo http://fr.slideshare.net/MichaelLaunay/20160911-novaideo-linnovation-participative-en-ligne

Le code de Nova-Ideo sous licence libre AGPL V3 est accessible sur : https://github.com/ecreall/nova-ideo

La vidéo filmée lors du PyConFR expliquant d'où vient Nova-Ideo et pourquoi il est libre : http://video-pyconfr2015.paulla.asso.fr/112_-_Michael_Launay_-_Nova-Ideo,_une_boite_a_idees_collaborative.html

Nous réalisons également une série de vidéos expliquant l'administration et le fonctionnement de Nova-Ideo accessible depuis la page Documentation de notre site https://www.nova-ideo.com/documentation .

Nous pouvons adapter Nova-Ideo à vos besoins spécifiques, alors n'hésitez pas à nous contacter, nous répondrons à vos questions !

Vous pouvez aussi faire part de vos remarques et proposer des évolutions en créant un compte sur https://evolutions.nova-ideo.com

Cordialement
L'équipe d'Ecréall
Services et Solutions en Logiciels Libres
Parc scientifique de la Haute Borne
Bâtiment Hub Innovation
11, rue de l'Harmonie
59650 Villeneuve d'Ascq
site : http://www.ecreall.com
tél : 03 20 79 32 90
mob : 06 16 85 91 12
Fax : 09 56 94 39 44
"""


INVITATION_SUBJECT = u"""Invitation à rejoindre la plateforme participative {novaideo_title}"""

INVITATION_MESSAGE = u"""
Bonjour,

{recipient_first_name} vous êtes invité à rejoindre la plateforme participative {novaideo_title} en tant que {roles}.

Pour valider votre invitation, vous devez cliquer sur le lien {invitation_url} et suivre les instructions.

""" + PORTAL_SIGNATURE


PRESENTATION_IDEA_SUBJECT = u"""Présentation de l'idée « {subject_title} »""" 


PRESENTATION_IDEA_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter l'idée « {subject_title} » figurant sur la plateforme {novaideo_title}. Cette idée est accessible à l'adresse : {subject_url}.

""" +  PORTAL_PRESENTATION + PORTAL_SIGNATURE


CONFIRMATION_SUBJECT = u"""Confirmation de votre inscription à la plateforme participative {novaideo_title}"""

CONFIRMATION_MESSAGE = u"""
Bienvenue sur la plateforme {novaideo_title}, nous vous confirmons votre inscription à la plateforme participative {novaideo_title}. 

Faites-nous part de vos idées en vous connectant à l'adresse {login_url}.

""" + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_SUBJECT = u"""Présentation de la proposition « {subject_title} »""" 


PRESENTATION_PROPOSAL_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter la proposition « {subject_title} » figurant sur la plateforme {novaideo_title}. Cette proposition est accessible à l'adresse : {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE


PRESENTATION_AMENDMENT_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter l'amendement « {subject_title} » figurant sur la plateforme {novaideo_title} sous {subject_url}.

""" + \
 PORTAL_PRESENTATION + PORTAL_SIGNATURE


PRESENTATION_AMENDMENT_SUBJECT = u"""« {subject_title} »"""


PRESENTATION_QUESTION_SUBJECT = u"""Présentation de la question « {subject_title} »""" 


PRESENTATION_QUESTION_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter la question « {subject_title} » figurant sur la plateforme {novaideo_title}. Cette question est accessible à l'adresse : {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE


PRESENTATION_ANSWER_SUBJECT = u"""Présentation de la réponse à une question « {subject_title} »""" 


PRESENTATION_ANSWER_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter la réponse à une question « {subject_title} » figurant sur la plateforme {novaideo_title}. Cette réponse est accessible à l'adresse : {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE


AMENDABLE_FIRST_SUBJECT = u"""Début du cycle d'amélioration de la proposition « {subject_title} »"""


AMENDABLE_FIRST_MESSAGE = u"""
Bonjour {recipient_first_name},

Vous êtes dorénavant trois participants au groupe de travail de la proposition « {subject_title} » qui se trouve sous {subject_url}, vous pouvez commencer à l'améliorer. 

Chaque participant peut faire des suggestions d'amélioration que les autres participants peuvent soit accepter, soit refuser. Lorsque le cycle d'amélioration est terminé, l'ensemble des participants votent soit pour continuer à améliorer la proposition, soit pour la soumettre à l'appréciation des membres de la plateforme.

Le cycle d'amélioration se termine le {duration}.

""" + PORTAL_SIGNATURE

AMENDABLE_SUBJECT = u"""Début du cycle d'amélioration de la proposition « {subject_title} »"""


AMENDABLE_MESSAGE = u"""
Bonjour {recipient_first_name},

Le groupe de travail sur la proposition « {subject_title} » qui se trouve sous {subject_url} a voté à la majorité pour continuer à améliorer la proposition.

Chaque participant peut faire des suggestions d'amélioration que les autres participants peuvent soit accepter, soit refuser. Lorsque le cycle d'amélioration est terminé, l'ensemble des participants votent soit pour continuer à améliorer la proposition, soit pour la soumettre à l'appréciation des membres de la plateforme.

Le cycle d'amélioration se termine le {duration}.

""" + PORTAL_SIGNATURE

ALERT_SUBJECT = u"""Fin du cycle d'amélioration de la proposition « {subject_title} » sans aucune amélioration"""

ALERT_MESSAGE = u"""
Bonjour {recipient_first_name},

Alors que le cycle d'amélioration est terminé, aucune amélioration n'a été apportée à la proposition « {subject_title} » qui se trouve sous {subject_url}. Vous allez devoir procéder au vote pour soumettre la proposition en l'état ou pour recommencer un nouveau cycle d'amélioration. 

""" + PORTAL_SIGNATURE

ALERT_END_SUBJECT = u"""Dernières améliorations avant la fin du cycle d'amélioration de la proposition « {subject_title} »"""

ALERT_END_MESSAGE = u"""
Bonjour {recipient_first_name},

Le cycle d'amélioration pour la proposition « {subject_title} » qui se trouve sous {subject_url} touche pratiquement à sa fin. Vous pouvez encore y apporter des améliorations, avant que le groupe de travail vote pour soumettre la proposition en l'état ou pour recommencer un nouveau cycle d'amélioration.

""" + PORTAL_SIGNATURE


RESULT_VOTE_AMENDMENT_SUBJECT = u"""Les résultats du vote sur les amendements liés à la proposition « {subject_title} » """

RESULT_VOTE_AMENDMENT_MESSAGE = u"""
<div>
Bonjour {recipient_first_name},

{message_result}
</div>
""" + PORTAL_SIGNATURE


PUBLISHPROPOSAL_SUBJECT = u"""Décision de soumettre la proposition « {subject_title} » à l'appréciation des membres de la plateforme"""

PUBLISHPROPOSAL_MESSAGE = u"""
Bonjour {recipient_first_name},

Le groupe de travail sur la proposition « {subject_title} » qui se trouve sous {subject_url} a voté à la majorité pour soumettre la proposition à l'appréciation des membres de la plateforme.

Chaque membre de la plateforme peut dorénavant soutenir ou s'opposer à la proposition et le Comité d'examen peut l'examiner.

""" + PORTAL_SIGNATURE


SYSTEM_CLOSE_PROPOSAL_SUBJECT = u"""Décision de cloturer la proposition « {subject_title} » à l'appréciation des membres de la plateforme"""

SYSTEM_CLOSE_PROPOSAL_MESSAGE = u"""
Bonjour {recipient_first_name},

Le groupe de travail sur la proposition « {subject_title} » qui se trouve sous {subject_url} n'est plus actif depuis quelques cycles de plus d'une semaine.
Pour cette raison, le groupe de travail a été dissout et la proposition est maintenant ouverte à un groupe de travail.

""" + PORTAL_SIGNATURE


VOTINGPUBLICATION_SUBJECT = u"""Début du vote pour améliorer la proposition « {subject_title} » ou la soumettre à l'appréciation des membres de la plateforme """

VOTINGPUBLICATION_MESSAGE = u"""
Bonjour {recipient_first_name},

Le cycle d'amélioration de la proposition « {subject_title} » qui se trouve sous {subject_url} est terminé, vous êtes invité à prendre part au vote pour améliorer la proposition ou la soumettre à l'appréciation des membres de la plateforme.

Vous disposez de 24 heures pour voter, après quoi le vote sera dépouillé en tenant compte du choix de la majorité des votants. Si aucun vote n'a lieu, un nouveau cycle d'amélioration commence pour une semaine.

""" + PORTAL_SIGNATURE


VOTINGAMENDMENTS_SUBJECT = u"""Début des votes sur les amendements portant sur la proposition « {subject_title} »"""

VOTINGAMENDMENTS_MESSAGE = u"""
Bonjour {recipient_first_name},

Les votes sur les amendements portant sur la proposition « {subject_title} » qui se trouve sous {subject_url} ont commencé. Merci de prendre part aux votes.

""" + PORTAL_SIGNATURE

WITHDRAW_SUBJECT = u"""Retrait de la liste d'attente du groupe de travail de la proposition « {subject_title} »"""

WITHDRAW_MESSAGE = u"""
Bonjour {recipient_first_name},

Vous ne faites plus partie de la liste d'attente du groupe de travail de la proposition {subject_title} » qui se trouve sous {subject_url}, suite à votre retrait de cette liste d'attente. 

Vous pourrez à tout moment chercher à rejoindre à nouveau le groupe de travail de la proposition, si elle est encore en cours d'amélioration.

""" + PORTAL_SIGNATURE

PARTICIPATE_WL_SUBJECT = u"""Participation au groupe de travail de la proposition « {subject_title} »"""

PARTICIPATE_WL_MESSAGE = u"""
Bonjour {recipient_first_name},

Vous faites partie du groupe de travail de la proposition {subject_title} » qui se trouve sous {subject_url}, suite au départ de l'un des participants. 

Vous pouvez en tant que participant au groupe de travail améliorer la proposition et vous pourrez, à la fin du cycle d'amélioration, voter pour continuer à l'améliorer ou la soumettre à l'appréciation des membres de la plateforme.

""" + PORTAL_SIGNATURE

PARTICIPATE_SUBJECT = u"""Votre participation au groupe de travail de la proposition « {subject_title} »"""

PARTICIPATE_MESSAGE = u"""
Bonjour {recipient_first_name},

Vous faites partie du groupe de travail de la proposition {subject_title} qui se trouve sous {subject_url}.

Vous pouvez en tant que participant au groupe de travail améliorer la proposition, s'il elle est en cours d'amélioration, et vous pourrez, à la fin du cycle d'amélioration, voter pour continuer à l'améliorer ou la soumettre à l'appréciation des membres de la plateforme.

""" + PORTAL_SIGNATURE

RESIGN_SUBJECT = u"""Votre départ du groupe de travail de la proposition « {subject_title} »"""

RESIGN_MESSAGE = u"""
Bonjour {recipient_first_name},

Nous vous confirmons que vous ne faites plus partie du groupe de travail de la proposition « {subject_title} » qui se trouve sous {subject_url}.

Vous pourrez à tout moment le rejoindre de nouveau, si vous ne faites pas partie déjà de cinq autres groupes de travail, qui est le nombre maximum de groupes de travail auxquels un membre a le droit de participer simultanément.

""" + PORTAL_SIGNATURE

WATINGLIST_SUBJECT = u"""Inscription sur la liste d'attente du groupe de travail de la proposition « {subject_title} »"""

WATINGLIST_MESSAGE = u"""
Bonjour {recipient_first_name},

Vous souhaitez participer au groupe de travail de la proposition « {subject_title} » qui se trouve sous {subject_url}, mais le nombre de participants a déjà atteint 12 personnes, qui est le nombre maximum de participants dans un groupe de travail.

Vous êtes sur la liste d'attente de ce groupe de travail et vous en ferez automatiquement partie, dès qu'une place se sera libérée.

""" + PORTAL_SIGNATURE


NEWCONTENT_SUBJECT = u"""{subject_type} « {subject_title} qui contient un des mots clés faisant partie de vos centres d'intérêt vient d'être publiée."""


NEWCONTENT_MESSAGE = u"""
Bonjour {recipient_first_name},

{subject_type} « {subject_title} » qui contient un des mots clés faisant partie de vos centres d'intérêt vient d'être publiée. Vous pouvez la consulter sous {subject_url}.

"""+ PORTAL_SIGNATURE


CONTENTMODIFIEF_SUBJECT = u"""{subject_type} « {subject_title} » qui fait partie de vos favoris vient de changer d'état"""


CONTENTMODIFIEF_MESSAGE = u"""
Bonjour {recipient_first_name},

{subject_type} « {subject_title} » qui fait partie de vos favoris vient de passer de l'état {state_source} à l'état {state_target}. Vous pouvez la consulter sous {subject_url}.

"""+ PORTAL_SIGNATURE


ARCHIVEIDEA_SUBJECT = u"""Décision des modérateurs d'archiver l'idée « {subject_title} »"""


ARCHIVEIDEA_MESSAGE = u"""
Bonjour {recipient_first_name},

L'idée « {subject_title} » vient d'être archivée par les modérateurs pour la raison suivante: 

{explanation}

Vous pouvez retrouver votre idée sous {subject_url}.

"""+ PORTAL_SIGNATURE

ARCHIVECONTENT_SUBJECT = u"""Décision des modérateurs d'archiver le contenu « {subject_title} »"""


ARCHIVECONTENT_MESSAGE = u"""
Bonjour {recipient_first_name},

Le contenu « {subject_title} » vient d'être archivée par les modérateurs pour la raison suivante: 

{explanation}

Vous pouvez retrouver votre contenu sous {subject_url}.

"""+ PORTAL_SIGNATURE


ARCHIVEPROPOSAL_SUBJECT = u"""Décision des modérateurs d'archiver la proposition « {subject_title} »"""


ARCHIVEPROPOSAL_MESSAGE = u"""
Bonjour {recipient_first_name},

La proposition « {subject_title} » vient d'être archivée par les modérateurs pour la raison suivante: 

{explanation}

Vous pouvez retrouver votre proposition sous {subject_url}.

"""+ PORTAL_SIGNATURE


ALERTOPINION_SUBJECT = u"""Avis du Comité d'examen sur la proposition « {subject_title} »"""


ALERTOPINION_MESSAGE = u"""
Bonjour {recipient_first_name},

Le Comité d'examen a émis un avis « {opinion} » sur la proposition « {subject_title} » avec l'explication suivante : « {explanation} ».

"""+ PORTAL_SIGNATURE


ALERTOPINIONIDEA_SUBJECT = u"""Avis d'un Examinateur sur l'idée « {subject_title} »"""


ALERTOPINIONIDEA_MESSAGE = u"""
Bonjour {recipient_first_name},

Un Examinateur a émis un avis « {opinion} » sur l'idée « {subject_title} » avec l'explication suivante : « {explanation} ».

"""+ PORTAL_SIGNATURE


PUBLISHEDIDEA_SUBJECT = u"""Décision des modérateurs de publier l'idée « {subject_title} »"""


PUBLISHEDIDEA_MESSAGE = u"""
Bonjour {recipient_first_name},

L'idée « {subject_title} » qui se trouve sous {subject_url} vient d'être publiée par les modérateurs sur la plateforme {novaideo_title}. Cette idée peut maintenant être utilisée par n'importe quel membre de la plateforme pour une proposition.

"""+ PORTAL_SIGNATURE


PUBLISHEDPROPOSAL_SUBJECT = u"""Décision des modérateurs de publier la proposition « {subject_title} »"""


PUBLISHEDPROPOSAL_MESSAGE = u"""
Bonjour {recipient_first_name},

La proposition « {subject_title} » qui se trouve sous {subject_url} vient d'être publiée par les modérateurs sur la plateforme {novaideo_title}.

"""+ PORTAL_SIGNATURE


PROPOSALREMOVED_SUBJECT = u"""Suppression de la proposition « {subject_title} »"""


PROPOSALREMOVED_MESSAGE = u"""
Bonjour {recipient_first_name},

La proposition « {subject_title} » viens d'être supprimée par les modérateurs pour le motif suivant:

« {explanation} »

"""+ PORTAL_SIGNATURE 


REFUSE_INVITATION_SUBJECT = u"""Refus de {user_first_name} {user_last_name} de rejoindre la plateforme {novaideo_title}"""


REFUSE_INVITATION_MESSAGE = u"""
Bonjour,

Nous vous signalons que {user_first_name} {user_last_name} a refusé votre invitation de rejoindre la plateforme {novaideo_title}.

"""+ PORTAL_SIGNATURE 


ACCEPT_INVITATION_SUBJECT = u"""Acceptation de {user_first_name} {user_last_name} de rejoindre la plateforme {novaideo_title}"""


ACCEPT_INVITATION_MESSAGE = u"""
Bonjour {recipient_first_name},

{user_first_name} {user_last_name} a accepté votre invitation de rejoindre la plateforme {novaideo_title}.

"""+ PORTAL_SIGNATURE


RESETPW_SUBJECT = u"""Votre nouveau mot de passe sur la plateforme {novaideo_title}"""


RESETPW_MESSAGE = u"""
Bonjour {recipient_first_name},

Vous souhaitez avoir un nouveau votre mot de passe sur la plateforme {novaideo_title}, merci de cliquer sur l'adresse {reseturl} et de saisir votre nouveau mot de passe.

"""+ PORTAL_SIGNATURE


PREREGISTRATION_SUBJECT = u"""Inscription à la plateforme participative {novaideo_title}"""


PREREGISTRATION_MESSAGE = u"""
Bonjour {recipient_first_name},

Vous avez été inscrit à la plateforme participative {novaideo_title}. Vous devez cliquer sur le lien {url} pour finaliser votre inscription. Ce lien a une durée de validité de 48 heures, votre inscription doit se faire avant le {deadline_date}.

"""+ PORTAL_SIGNATURE


ADMIN_PREREGISTRATION_SUBJECT = u"""Inscription à la plateforme participative {novaideo_title}"""


ADMIN_PREREGISTRATION_MESSAGE = u"""
Bonjour {recipient_first_name},

Une nouvelle inscription à la plateforme participative {novaideo_title} vient d'être ajoutée. L'inscription est sous {url}. Vous devez donner votre avis pour la modérer.

"""+ PORTAL_SIGNATURE


ALERTCOMMENT_SUBJECT = u"""Nouveau commentaire sur {subject_type} « {subject_title} »"""


ALERTCOMMENT_MESSAGE = u"""
Bonjour {recipient_first_name},

Un nouveau commentaire a été fait sur {subject_type} « {subject_title} ».

"{comment_content}"

Vous pouvez le retrouver sous {comment_url} et lui apporter une réponse.

"""+ PORTAL_SIGNATURE


ALERTANSWER_SUBJECT = u"""Nouvelle réponse sur {subject_type} « {subject_title} »"""


ALERTANSWER_MESSAGE = u"""
Bonjour {recipient_first_name},

Une nouvelle réponse a été donnée à {subject_type} « {subject_title} ».

"{comment_content}"

Vous pouvez le retrouver sous {comment_url} et lui apporter une réponse.

"""+ PORTAL_SIGNATURE

ALERTDISCUSS_SUBJECT = u"""Nouveau message ajouté à votre discussion avec « {subject_title} »"""


ALERTDISCUSS_MESSAGE = u"""
Bonjour {recipient_first_name},

Un nouveau message a été ajouté à votre discussion avec « {subject_title} ».

"{comment_content}"

Vous pouvez le retrouver sous {comment_url} et lui apporter une réponse.

"""+ PORTAL_SIGNATURE

ALERTRESPONS_SUBJECT = u"""Une personne a donné une réponse à un commentaire sur {subject_type} « {subject_title} »"""


ALERTRESPONS_MESSAGE = u"""
Bonjour {recipient_first_name},

Une personne a donné une réponse à un commentaire sur {subject_type} « {subject_title} » qui se trouve sous {comment_url}.

"{comment_content}"

"""+ PORTAL_SIGNATURE


NEWSLETTER_SUBSCRIPTION_SUBJECT = u"""Inscription newsletter"""

NEWSLETTER_SUBSCRIPTION_MESSAGE = u"""
Bonjour {first_name} {last_name},

Vous êtes maintenant abonné à la newsletter {newsletter_title}.

""" + PORTAL_SIGNATURE

NEWSLETTER_UNSUBSCRIPTION_SUBJECT = u"""Désinscription de la newsletter"""

NEWSLETTER_UNSUBSCRIPTION_MESSAGE = u"""
Bonjour {first_name} {last_name},

Vous êtes maintenant désabonné de la newsletter {newsletter_title}.

""" + PORTAL_SIGNATURE


PUBLISHEDCHALLENGE_SUBJECT = u"""Décision des modérateurs de publier le challenge « {subject_title} »"""


PUBLISHEDCHALLENGE_MESSAGE = u"""
Bonjour {recipient_first_name},

Le challenge « {subject_title} » qui se trouve sous {subject_url} vient d'être publiée par les modérateurs sur la plateforme {novaideo_title}.

"""+ PORTAL_SIGNATURE

ARCHIVECHALLENGE_SUBJECT = u"""Décision des modérateurs d'archiver le challenge « {subject_title} »"""


ARCHIVECHALLENGE_MESSAGE = u"""
Bonjour {recipient_first_name},

Le challenge « {subject_title} » vient d'être archivée par les modérateurs pour la raison suivante: 

{explanation}

Vous pouvez retrouver votre challenge sous {subject_url}.

"""+ PORTAL_SIGNATURE


PRESENTATION_CHALLENGE_SUBJECT = u"""Présentation du challenge « {subject_title} »""" 


PRESENTATION_CHALLENGE_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter le challenge « {subject_title} » figurant sur la plateforme {novaideo_title}. Ce challenge est accessible à l'adresse : {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE


FIRST_INVITATION = {
    'subject': FIRST_INVITATION_SUBJECT,
    'template': FIRST_INVITATION_MESSAGE
}


DEFAULT_SITE_MAILS = {
    'invitation': {
              'title': _("Invitation"),
              'subject': INVITATION_SUBJECT,
              'template': INVITATION_MESSAGE
    },
    'refuse_invitation': {
              'title': _("Refuse the invitation"),
              'subject': REFUSE_INVITATION_SUBJECT,
              'template': REFUSE_INVITATION_MESSAGE
    },
    'accept_invitation': {
              'title': _("Accept the invitation"),
              'subject': ACCEPT_INVITATION_SUBJECT,
              'template': ACCEPT_INVITATION_MESSAGE
    },
    'reset_password': {
              'title': _("Reset the password"),
              'subject': RESETPW_SUBJECT,
              'template': RESETPW_MESSAGE
    },
    'registration_confiramtion': {
              'title': _("Registration confirmation"),
              'subject': CONFIRMATION_SUBJECT,
              'template': CONFIRMATION_MESSAGE
    },
    'preregistration': {
              'title': _("Pre-registration of users"),
              'subject': PREREGISTRATION_SUBJECT,
              'template': PREREGISTRATION_MESSAGE
    },

    'presentation_idea': {
              'title': _("Presentation of an idea"),
              'subject': PRESENTATION_IDEA_SUBJECT,
              'template': PRESENTATION_IDEA_MESSAGE
    },

    'presentation_proposal': {
              'title': _("Presentation of a proposal"),
              'subject': PRESENTATION_PROPOSAL_SUBJECT,
              'template': PRESENTATION_PROPOSAL_MESSAGE
    },
    'presentation_amendment': {
              'title': _('Presentation of an amendment'),
              'subject': PRESENTATION_AMENDMENT_SUBJECT,
              'template': PRESENTATION_AMENDMENT_MESSAGE
    },
    'first_start_work': {
              'title': _('Start of the improvement cycle'),
              'subject': AMENDABLE_FIRST_SUBJECT,
              'template': AMENDABLE_FIRST_MESSAGE
    },
    'start_work': {
              'title': _('Start of the improvement cycle'),
              'subject': AMENDABLE_SUBJECT,
              'template': AMENDABLE_MESSAGE
    },
    'alert_amendment': {
              'title': _("Inactivity alert"),
              'subject': ALERT_SUBJECT,
              'template': ALERT_MESSAGE
    },
    'alert_end': {
              'title': _("End of the improvement cycle"),
              'subject': ALERT_END_SUBJECT,
              'template': ALERT_END_MESSAGE
    },
    'vote_amendment_result': {
              'title': _("Result of the ballot (amendments)"),
              'subject': RESULT_VOTE_AMENDMENT_SUBJECT,
              'template': RESULT_VOTE_AMENDMENT_MESSAGE
    },
    'publish_proposal': {
              'title': _("Publication of the proposal"),
              'subject': PUBLISHPROPOSAL_SUBJECT,
              'template': PUBLISHPROPOSAL_MESSAGE
    },
    'start_vote_publishing': {
              'title': _("Start of the ballot (publication of the proposal)"),
              'subject': VOTINGPUBLICATION_SUBJECT,
              'template': VOTINGPUBLICATION_MESSAGE
    },
    'start_vote_amendments': {
              'title': _("Start of the ballot (amendments)"),
              'subject': VOTINGAMENDMENTS_SUBJECT,
              'template': VOTINGAMENDMENTS_MESSAGE
    },
    'withdeaw': {
              'title': _("Withdraw"),
              'subject': WITHDRAW_SUBJECT,
              'template': WITHDRAW_MESSAGE
    },
    'wg_wating_list_participation': {
              'title': _("Automatic addition of a participant in the working group that was on the waiting list"),
              'subject': PARTICIPATE_WL_SUBJECT,
              'template': PARTICIPATE_WL_MESSAGE
    },
    'wg_participation': {
              'title': _("Participation in the working group"),
              'subject': PARTICIPATE_SUBJECT,
              'template': PARTICIPATE_MESSAGE
    },
    'wg_resign': {
              'title': _("Resignation from the working group"),
              'subject': RESIGN_SUBJECT,
              'template': RESIGN_MESSAGE
    },
    'wating_list': {
              'title': _("Registration on the waiting list"),
              'subject': WATINGLIST_SUBJECT,
              'template': WATINGLIST_MESSAGE
    },
    'alert_new_content': {
              'title': _("Alert (new content)"),
              'subject': NEWCONTENT_SUBJECT,
              'template': NEWCONTENT_MESSAGE
    },
    'alert_content_modified': {
              'title': _("Alert (content modified)"),
              'subject': CONTENTMODIFIEF_SUBJECT,
              'template': CONTENTMODIFIEF_MESSAGE
    },
    'archive_idea_decision': {
              'title': _("Moderation: Archive the idea"),
              'subject': ARCHIVEIDEA_SUBJECT,
              'template': ARCHIVEIDEA_MESSAGE
    },
    'opinion_proposal': {
              'title': _("Moderation: Opinion on the proposal"),
              'subject': ALERTOPINION_SUBJECT,
              'template': ALERTOPINION_MESSAGE
    },
    'opinion_idea': {
              'title': _("Moderation: Opinion on the idea"),
              'subject': ALERTOPINIONIDEA_SUBJECT,
              'template': ALERTOPINIONIDEA_MESSAGE
    },
    'publish_idea_decision': {
              'title': _("Moderation: Publish the idea"),
              'subject': PUBLISHEDIDEA_SUBJECT,
              'template': PUBLISHEDIDEA_MESSAGE
    },
    'archive_proposal_decision': {
              'title': _("Moderation: Archive the proposal"),
              'subject': ARCHIVEPROPOSAL_SUBJECT,
              'template': ARCHIVEPROPOSAL_MESSAGE
    },
    'publish_proposal_decision': {
              'title': _("Moderation: Publish the proposal"),
              'subject': PUBLISHEDPROPOSAL_SUBJECT,
              'template': PUBLISHEDPROPOSAL_MESSAGE
    },
    'delete_proposal': {
              'title': _("Moderation: Delete the proposal"),
              'subject': PROPOSALREMOVED_SUBJECT,
              'template': PROPOSALREMOVED_MESSAGE
    },
    'alert_comment': {
              'title': _("Warning: new comment"),
              'subject': ALERTCOMMENT_SUBJECT,
              'template': ALERTCOMMENT_MESSAGE
    },
    'alert_discuss': {
              'title': _("Warning: new discussion"),
              'subject': ALERTDISCUSS_SUBJECT,
              'template': ALERTDISCUSS_MESSAGE
    },
    'alert_respons': {
              'title': _("Alert: answer"),
              'subject': ALERTRESPONS_SUBJECT,
              'template': ALERTRESPONS_MESSAGE
    },
    'newsletter_subscription': {
              'title': _("Subscription to the newsletter"),
              'subject': NEWSLETTER_SUBSCRIPTION_SUBJECT,
              'template': NEWSLETTER_SUBSCRIPTION_MESSAGE
    },
    'newsletter_unsubscription': {
              'title': _("Unsubscription from the newsletter"),
              'subject': NEWSLETTER_UNSUBSCRIPTION_SUBJECT,
              'template': NEWSLETTER_UNSUBSCRIPTION_MESSAGE
    },
    'moderate_preregistration': {
              'title': _("New registration"),
              'subject': ADMIN_PREREGISTRATION_SUBJECT,
              'template': ADMIN_PREREGISTRATION_MESSAGE
    },
    'close_proposal': {
              'title': _("Close the proposal"),
              'subject': SYSTEM_CLOSE_PROPOSAL_SUBJECT,
              'template': SYSTEM_CLOSE_PROPOSAL_MESSAGE
    },

    'presentation_question': {
              'title': _("Presentation of a question"),
              'subject': PRESENTATION_QUESTION_SUBJECT,
              'template': PRESENTATION_QUESTION_MESSAGE
    },

    'presentation_answer': {
              'title': _("Presentation of an answer"),
              'subject': PRESENTATION_ANSWER_SUBJECT,
              'template': PRESENTATION_ANSWER_MESSAGE
    },
    'alert_answer': {
              'title': _("Warning: new answer"),
              'subject': ALERTANSWER_SUBJECT,
              'template': ALERTANSWER_MESSAGE
    },
    'archive_content_decision': {
              'title': _("Moderation: Archive the content"),
              'subject': ARCHIVECONTENT_SUBJECT,
              'template': ARCHIVECONTENT_MESSAGE
    },
    'archive_challenge_decision': {
              'title': _("Moderation: Archive the challenge"),
              'subject': ARCHIVECHALLENGE_SUBJECT,
              'template': ARCHIVECHALLENGE_MESSAGE
    },
    'publish_challenge_decision': {
              'title': _("Moderation: Publish the challenge"),
              'subject': PUBLISHEDCHALLENGE_SUBJECT,
              'template': PUBLISHEDCHALLENGE_MESSAGE
    },

    'presentation_challenge': {
              'title': _("Presentation of a challenge"),
              'subject': PRESENTATION_CHALLENGE_SUBJECT,
              'template': PRESENTATION_CHALLENGE_MESSAGE
    }
}
