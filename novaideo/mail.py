# -*- coding: utf8 -*-
""" The contents of e-mails"""

PORTAL_SIGNATURE = """
Cordialement,
                                                                                
La Plateforme NovaIdeo
"""

INVITATION_MESSAGE = u"""
Bonjour,

{user_title} {invitation.last_name} vous êtes invité à rejoindre l\'application collaborative INEUS en tant que {roles}. Veuilliez visiter ce lien {invitation_url} afin de valider votre invitation.
""" + PORTAL_SIGNATURE


PRESENTATION_IDEA_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

{my_last_name} souhaite vous présenter l'idée figurant sur la plateforme Nova-Ideo.org sous {subject_url}. Nova-Ideo est une application participative permettant à tout membre d'un collectif d'initier des idées, les reprendre dans des propositions, constituer des groupes de travail pour améliorer ces propositions et les finaliser, avoir l'appréciation des membres de la communauté et l'avis de comités d'examen.
""" + PORTAL_SIGNATURE

PRESENTATION_IDEA_SUBJECT = u"""Présentation : {subject_title}""" 


CONFIRMATION_SUBJECT = u"""Confirmation de votre inscription"""

CONFIRMATION_MESSAGE = u"""
Bonjour {user_title} {person.last_name},

Bienvenue sur l'application NovaIdeo. L'accès à l'application se fait sous {login_url}. Pour y ajouter des idées ou des propositions, vous devez préalablement vous identifier avec votre courriel et votre mot de passe.
""" + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

{my_title} {my_last_name} souhaite vous présenter la proposition figurant sur la plateforme Nova-Ideo.org sous {subject_url}. Nova-Ideo est un service en ligne permettant d'initier des propositions, constituer des groupes de travail pour les améliorer et les finaliser, bénéficier de soutiens de membres de la communauté et d'avis de comités d'examen.
""" + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_SUBJECT = u"""Présentation : {subject_title}""" 


PRESENTATION_AMENDMENT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

{my_title} {my_last_name} souhaite vous présenter l'amendment figurant sur la plateforme Nova-Ideo.org sous {subject_url}. Nova-Ideo est un service en ligne permettant d'initier des propositions, constituer des groupes de travail pour les améliorer et les finaliser, bénéficier de soutiens de membres de la communauté et d'avis de comités d'examen.
""" + PORTAL_SIGNATURE


PRESENTATION_AMENDMENT_SUBJECT = u"""Présentation : {subject_title}"""


ALERT_SUBJECT = u"""Inactivité : {subject_title}"""

ALERT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Alors que la durée du cycle d'amélioration a expiré, aucun amendement n'a été soumis pour la proposition \"{subject_title}\" qui se trouve sous {subject_url}. Vous allez devoir procéder au vote pour soumettre au collectif la proposition en l'état ou pour commencer un nouveau cycle d'amélioration. 

""" + PORTAL_SIGNATURE

RESULT_VOTE_AMENDMENT_SUBJECT = u"""Les résultats du vote sur les amendements liés à la proposition \"{subject_title}\" """

RESULT_VOTE_AMENDMENT_MESSAGE = u"""
<div>
Bonjour {recipient_title} {recipient_last_name},

{message_result}
</div>
""" + PORTAL_SIGNATURE


PUBLISHPROPOSAL_SUBJECT = u"""Publication : {subject_title}"""

PUBLISHPROPOSAL_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

La proposition {subject_title} ({subject_url}) est publiée.

""" + PORTAL_SIGNATURE


VOTINGPUBLICATION_SUBJECT = u"""Début de vote pour soumettre au collectif la proposition \"{subject_title}\" """

VOTINGPUBLICATION_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Le vote pour soumettre au collectif la proposition \"{subject_title}\" qui se trouve sous {subject_url} a commencé. Merci de prendre part au vote.

""" + PORTAL_SIGNATURE


VOTINGAMENDMENTS_SUBJECT = u"""Debut de vote sur les amendements : {subject_title}"""

VOTINGAMENDMENTS_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Le vote sur les amendements de la proposition {subject_title} ({subject_url}) a commencé.

""" + PORTAL_SIGNATURE

WITHDRAW_SUBJECT = u"""Désinscription de la liste d'attente: {subject_title}"""

WITHDRAW_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Vous ne faite plus partie de la liste d'attente du groupe de travail de la proposition {subject_title} ({subject_url}).

""" + PORTAL_SIGNATURE

PARTICIPATE_SUBJECT = u"""Participation au groupe de travail sur la proposition \"{subject_title}\" """

PARTICIPATE_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Vous faites partie du groupe de travail sur la proposition \"{subject_title}\" qui se trouve sous {subject_url}. Dès que trois participants ont rejoint le groupe de travail, vous pourrez participer au vote pour soumettre au collectif la proposition.

""" + PORTAL_SIGNATURE

RESIGN_SUBJECT = u"""Démission du groupe de travail sur la proposition \"{subject_title}\" """

RESIGN_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Vous avez quitté le groupe de travail sur la proposition \"{subject_title}\"  qui se trouve sous ({subject_url}). S'il est ouvert, vous pourrez de nouveau le rejoindre en cliquant sur l'action "Participer".

""" + PORTAL_SIGNATURE

WATINGLIST_SUBJECT = u"""Partcipation au groupe de travail : {subject_title}"""

WATINGLIST_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Vous faite partie de la liste d'attente du groupe de travail de la proposition {subject_title} ({subject_url}).

""" + PORTAL_SIGNATURE