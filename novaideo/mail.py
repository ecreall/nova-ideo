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
Bonjour {member_title} {member_first_name} {member_last_name},

{user_title} {user_first_name} {user_last_name} souhaite vous présenter l'Idée figurant sur la plateforme Nova-Ideo.org sous {idea_url}. Nova-Ideo est un service en ligne permettant d'initier des propositions, constituer des groupes de travail pour les améliorer et les finaliser, bénéficier de soutiens de membres de la communauté et d'avis de comités d'examen.
""" + PORTAL_SIGNATURE


CONFIRMATION_MESSAGE = u"""
Bonjour {person.user_title} {person.last_name} {person.first_name},

Bienvenue sur le plateforme NovaIdeo.
""" + PORTAL_SIGNATURE
