# -*- coding: utf8 -*-


PORTAL_SIGNATURE = """

Cordialement,
                                                                                
La Plateforme NovaIdeo
"""


INVITATION_MESSAGE = u"""
Bonjour,

{user_title} {invitation.last_name} {invitation.first_name} vous êtes invité à rejoindre l\'application collaborative INEUS en tant que {roles}. Veuilliez visiter ce lien {invitation_url} afin de valider votre invitation.
""" + PORTAL_SIGNATURE


PRESENTATION_IDEA_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

{my_title} {my_first_name} {my_last_name} souhaite vous présenter l'Idée figurant sur la plateforme Nova-Ideo.org sous {subject_url}. Nova-Ideo est un service en ligne permettant d'initier des propositions, constituer des groupes de travail pour les améliorer et les finaliser, bénéficier de soutiens de membres de la communauté et d'avis de comités d'examen.
""" + PORTAL_SIGNATURE

PRESENTATION_IDEA_SUBJECT = u"""Présentation : {subject_title}""" 

CONFIRMATION_MESSAGE = u"""
Bonjour {person.user_title} {person.last_name} {person.first_name},

Bienvenue sur le plateforme NovaIdeo.
""" + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

{my_title} {my_first_name} {my_last_name} souhaite vous présenter la proposition figurant sur la plateforme Nova-Ideo.org sous {subject_url}. Nova-Ideo est un service en ligne permettant d'initier des propositions, constituer des groupes de travail pour les améliorer et les finaliser, bénéficier de soutiens de membres de la communauté et d'avis de comités d'examen.
""" + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_SUBJECT = u"""Présentation : {subject_title}""" 


PRESENTATION_AMENDMENT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

{my_title} {my_first_name} {my_last_name} souhaite vous présenter l'amendment figurant sur la plateforme Nova-Ideo.org sous {subject_url}. Nova-Ideo est un service en ligne permettant d'initier des propositions, constituer des groupes de travail pour les améliorer et les finaliser, bénéficier de soutiens de membres de la communauté et d'avis de comités d'examen.
""" + PORTAL_SIGNATURE


PRESENTATION_AMENDMENT_SUBJECT = u"""Présentation : {subject_title}"""


ALERT_SUBJECT= u"""Inactivité : {subject_title}"""

ALERT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

Aucun amendement n'a été publié pour la proposition sous {subject_url}.

""" + PORTAL_SIGNATURE


RESULT_VOTE_AMENDMENT_SUBJECT= u"""Les resultat du vote sur amendments : {subject_title}"""

RESULT_VOTE_AMENDMENT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

Les résultats du vote sur amendements concernant la proposition {subject_title} ({subject_url}) sont les suivants:

{message_result}

Les amendements élus, après calcule, du vote:

{electeds_result}

""" + PORTAL_SIGNATURE


PUBLISHPROPOSAL_SUBJECT= u"""Publication : {subject_title}"""

PUBLISHPROPOSAL_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

La proposition {subject_title} ({subject_url}) est publiée.

""" + PORTAL_SIGNATURE


VOTINGPUBLICATION_SUBJECT= u"""Debut de vote sur la publication : {subject_title}"""

VOTINGPUBLICATION_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

Le vote sur publication de la proposition {subject_title} ({subject_url}) a commencé.

""" + PORTAL_SIGNATURE


VOTINGAMENDMENTS_SUBJECT= u"""Debut de vote sur les amendements : {subject_title}"""

VOTINGAMENDMENTS_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

Le vote sur les amendements de la proposition {subject_title} ({subject_url}) a commencé.

""" + PORTAL_SIGNATURE


WITHDRAW_SUBJECT= u"""Désinscription de la liste d'attente: {subject_title}"""

WITHDRAW_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

Vous ne faite plus partie de la liste d'attente du groupe de travail de la proposition {subject_title} ({subject_url}).

""" + PORTAL_SIGNATURE


PARTICIPATE_SUBJECT= u"""Partcipation au groupe de travail : {subject_title}"""

PARTICIPATE_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

Vous faite partie du groupe de travail de la proposition {subject_title} ({subject_url}).

""" + PORTAL_SIGNATURE


RESIGN_SUBJECT= u"""Démission du groupe de travail : {subject_title}"""

RESIGN_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

Vous ne faite plus partie du groupe de travail de la proposition {subject_title} ({subject_url}).

""" + PORTAL_SIGNATURE


WATINGLIST_SUBJECT= u"""Partcipation au groupe de travail : {subject_title}"""

WATINGLIST_MESSAGE = u"""
Bonjour {recipient_title} {recipient_first_name} {recipient_last_name},

Vous faite partie de la liste d'attente du groupe de travail de la proposition {subject_title} ({subject_url}).

""" + PORTAL_SIGNATURE
