# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

""" The contents of e-mails"""

PORTAL_SIGNATURE = """Cordialement,
                                                                                
La Plateforme {novaideo_title}
"""
PORTAL_PRESENTATION = u"""{novaideo_title} est une plateforme participative qui permet à tout membre d'initier des idées pouvant être utilisées dans des propositions travaillées collectivement. Une fois finalisées, ces propositions peuvent être soumises à l'appréciation des membres et faire l'objet d'une décision d'un comité d'examen.

"""

INVITATION_MESSAGE = u"""
Bonjour ,

{user_title} {invitation.last_name} vous êtes invité à rejoindre l\'application collaborative {novaideo_title} en tant que {roles}. Veuilliez visiter ce lien {invitation_url} afin de valider votre invitation.
""" + PORTAL_SIGNATURE


PRESENTATION_IDEA_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter l'idée « {subject_title} » figurant sur la plateforme {novaideo_title} sous {subject_url}.""" + \
 PORTAL_PRESENTATION + PORTAL_SIGNATURE

PRESENTATION_IDEA_SUBJECT = u"""{subject_title}""" 


CONFIRMATION_SUBJECT = u"""Confirmation de votre inscription"""

CONFIRMATION_MESSAGE = u"""
Bonjour,

Bienvenue sur la plateforme {novaideo_title}. L'accès à la plateforme se fait sous {login_url}. Pour y ajouter des idées ou des propositions, vous devez préalablement vous identifier avec votre courriel et votre mot de passe.

""" + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter la proposition {subject_title} figurant sur la plateforme {novaideo_title} sous {subject_url}.""" + \
 PORTAL_PRESENTATION + PORTAL_SIGNATURE


PRESENTATION_PROPOSAL_SUBJECT = u"""{subject_title}""" 


PRESENTATION_AMENDMENT_MESSAGE = u"""
Bonjour,

{my_first_name} {my_last_name} souhaite vous présenter l'amendement {subject_title} figurant sur la plateforme {novaideo_title} sous {subject_url}.

""" + \
 PORTAL_PRESENTATION + PORTAL_SIGNATURE


PRESENTATION_AMENDMENT_SUBJECT = u"""{subject_title}"""


AMENDABLE_SUBJECT = u"""Début du cycle d'amélioration de la proposition {subject_title}"""


AMENDABLE_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Le groupe de travail sur la proposition {subject_title} a voté pour commencer un cycle d'amélioration, ce groupe de travail est actuellement {isclosed}. Les étapes de ce cyle d'amélioration sont l'amélioration de la proposition sous forme d'amendements, les votes sur ces amendements et le vote pour soumettre la proposition amendée en l'état ou non. La fin du cycle d'amélioration est prévue le {duration}.

""" + PORTAL_SIGNATURE


PROOFREADING_SUBJECT = u"""Début du cycle d'amélioration de la proposition {subject_title}"""


PROOFREADING_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Le groupe de travail sur la proposition {subject_title} a voté pour commencer un cycle d'amélioration, ce groupe de travail est actuellement {isclosed}. Les étapes de ce cyle d'amélioration sont la relecture de la proposition, son amélioration sous forme d'amendements, les votes sur ces amendements et le vote pour soumettre la proposition amendée en l'état ou non. La fin du cycle d'amélioration est prévue le {duration}.

""" + PORTAL_SIGNATURE


ALERT_SUBJECT = u"""Aucun amendement sur la proposition {subject_title}"""

ALERT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Alors que le cycle d'amélioration est terminé, aucun amendement n'a été soumis pour la proposition \"{subject_title}\" qui se trouve sous {subject_url}. Vous allez devoir procéder au vote pour soumettre la proposition en l'état ou pour commencer un nouveau cycle d'amélioration. 

""" + PORTAL_SIGNATURE

RESULT_VOTE_AMENDMENT_SUBJECT = u"""Les résultats du vote sur les amendements liés à la proposition \"{subject_title}\" """

RESULT_VOTE_AMENDMENT_MESSAGE = u"""
<div>
Bonjour {recipient_title} {recipient_last_name},

{message_result}
</div>
""" + PORTAL_SIGNATURE


PUBLISHPROPOSAL_SUBJECT = u"""Publication de la proposition {subject_title}"""

PUBLISHPROPOSAL_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

La proposition {subject_title} qui se trouve sous {subject_url} est publiée. Pour la soumettre en l'état ou commencer un cycle d'amélioration, un groupe de travail d'au moins trois personnes doit être constitué.

""" + PORTAL_SIGNATURE


VOTINGPUBLICATION_SUBJECT = u"""Début des votes pour soumettre en l'état la proposition \"{subject_title}\" """

VOTINGPUBLICATION_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Les votes pour soumettre en l'état la proposition \"{subject_title}\" qui se trouve sous {subject_url} ont commencé. Merci de prendre part aux votes.

""" + PORTAL_SIGNATURE


VOTINGAMENDMENTS_SUBJECT = u"""Début des votes sur les amendements portant sur la proposition {subject_title}"""

VOTINGAMENDMENTS_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Les votes sur les amendements portant sur la proposition {subject_title} qui se trouve sous {subject_url} ont commencé. Merci de prendre part aux votes.

""" + PORTAL_SIGNATURE

WITHDRAW_SUBJECT = u"""Désinscription de la liste d'attente concernant la proposition {subject_title}"""

WITHDRAW_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Pour information, vous ne faites plus partie de la liste d'attente du groupe de travail de la proposition {subject_title} qui se trouve sous {subject_url}. 

""" + PORTAL_SIGNATURE

PARTICIPATE_SUBJECT = u"""Participation au groupe de travail sur la proposition \"{subject_title}\" """

PARTICIPATE_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Pour information, vous faites partie du groupe de travail sur la proposition \"{subject_title}\" qui se trouve sous {subject_url}. Dès que le groupe de travail a atteint trois participants, vous pourrez participer aux votes pour soumettre la proposition en l'état ou au contraire commencer un cycle d'amélioration.

""" + PORTAL_SIGNATURE

RESIGN_SUBJECT = u"""Démission du groupe de travail sur la proposition \"{subject_title}\" """

RESIGN_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Vous avez décidé de quitter le groupe de travail sur la proposition \"{subject_title}\" qui se trouve sous {subject_url}. S'il est ouvert, vous pourrez décider de le rejoindre de nouveau en cliquant sur l'action "Participer".

""" + PORTAL_SIGNATURE

WATINGLIST_SUBJECT = u"""Participation au groupe de travail sur la proposition {subject_title}"""

WATINGLIST_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

Pour information, vous faites partie de la liste d'attente du groupe de travail sur la proposition {subject_title} qui se trouve sous {subject_url}. Si le groupe de travail atteint moins de 12 personnes et si le ne vous faites pas partie de plus de 5 groupes de travail, vous y serez immédiatement ajouté en tant que participant. 

""" + PORTAL_SIGNATURE


NEWCONTENT_SUBJECT = u"""Un contenu vient d'être publié"""


NEWCONTENT_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

{subject_type} {subject_title} qui contient un des mots clés faisant partie de vos centres d'intérêt vient d'être publiée. Vous pouvez la consulter sous {subject_url}

"""+ PORTAL_SIGNATURE


ARCHIVEIDEA_SUBJECT = u"""Décision des modérateur sur l'idée {subject_title}"""


ARCHIVEIDEA_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

L'idée {subject_title} viens d'être archivée par les modérateurs pour la raison suivante: 

{explanation}

"""+ PORTAL_SIGNATURE


ALERTOPINION_SUBJECT = u"""Avis des modérateur sur la proposition {subject_title}"""


ALERTOPINION_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

les modérateurs ont émis un avis {opinion} sur la proposition {subject_title}: 

{explanation}

"""+ PORTAL_SIGNATURE


PUBLISHEDIDEA_SUBJECT = u"""Décision des modérateur sur l'idée {subject_title}"""


PUBLISHEDIDEA_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

L'idée {subject_title} viens d'être publiée par les modérateurs.

"""+ PORTAL_SIGNATURE


PROPOSALREMOVED_SUBJECT = u"""Suppression de la proposition {subject_title}"""


PROPOSALREMOVED_MESSAGE = u"""
Bonjour {recipient_title} {recipient_last_name},

La proposition {subject_title} viens d'être supprimée par les modérateurs pour le motif suivant.
{explanation}

"""+ PORTAL_SIGNATURE 


REFUSE_INVITATION_SUBJECT = u"""Refus de {user_first_name} {user_last_name} de rejoindre la plateforme {novaideo_title}"""


REFUSE_INVITATION_MESSAGE = u"""
{user_title} {user_first_name} {user_last_name} a refusé votre invitation de rejoindre la plateforme {novaideo_title}.

"""+ PORTAL_SIGNATURE 


ACCEPT_INVITATION_SUBJECT = u"""Acceptation de {user_first_name} {user_last_name} de rejoindre la plateforme {novaideo_title}"""


ACCEPT_INVITATION_MESSAGE = u"""
{user_title} {user_first_name} {user_last_name} a accepté votre invitation de rejoindre la plateforme {novaideo_title}.

"""+ PORTAL_SIGNATURE
