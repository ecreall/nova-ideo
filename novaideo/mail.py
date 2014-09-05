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

Les résultats du vote sur amendements concernant la proposition {subject_url} sont les suivants:

{message_result}

Les amendements élus, après calcule, du vote:

{electeds_result}

""" + PORTAL_SIGNATURE

