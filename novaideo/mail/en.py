# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi, *

from . import add_mail_template

""" The contents of e-mails"""

PORTAL_SIGNATURE = """Kind regards,

The {novaideo_title} platform.
"""

PORTAL_PRESENTATION = u"""{novaideo_title} is a participatory platform with which any member can initiate ideas. These ideas can then be improved in spontaneous working groups. Once improved and adopted by the working group, these proposals are subject to the appreciation of all members, and be the purpose of the decision of an examination committee.

"""

FIRST_INVITATION_SUBJECT = u"""Invitation to join the Nova-Ideo participatory platform"""

FIRST_INVITATION_MESSAGE = u"""
Dear,


We thank you for your interest in Nova-Ideo.

{recipient_first_name} your are invited to join the the Nova-Ideo participatory platform as the site administrator.

In order to validate your invitation, you must click on the following link {invitation_url} and follow the instructions.

We remind you that Nova-Ideo is an on-line participatory innovation solution, which addresses the following problems:
- you want to implement a participatory innovation solution;
- you already have an "ideas box", and it is either empty, or so full that it is impossible to find the good ideas;
- you have no time to manage ideas. Thereby, you miss many opportunities, and create disappointment among those who have good ideas.

With Nova-Ideo, you will: collect the ideas of a set of people, find the good ones and transform them into implementable proposals that reflect all points of view.

To do so, Nova-Ideo uses crowdsourcing, by having the "crowd" to work on the transformation of ideas into full proposals.

Nova-Ideo merges the best of the "ideas box", of the collaborative portal, and of internal communication tools. It proposes cutting-edge social innovation solutions such as the majority judgement or the management of the rarity of supports/rejections.

Look at our web page https://www.nova-ideo.com and specifically its Documentation page https://www.nova-ideo.com/documentation

Follow our Twitter account: https://twitter.com/NovaIdeo

You can look at our detailed presentation of Nova-Ideo http://fr.slideshare.net/MichaelLaunay/20160911-novaideo-linnovation-participative-en-ligne

The source code of Nova-Ideo is available under the free AGPL V3 licence is available at: https://github.com/ecreall/nova-ideo

The video recording of the the PyConFR conference explaining where Nova-Ideo comes from, and why it is free: http://video-pyconfr2015.paulla.asso.fr/112_-_Michael_Launay_-_Nova-Ideo,_une_boite_a_idees_collaborative.html

We currently develope a seris of videos explaining the administration and the operation of Nova-Ideo. It can be accessed from the Documentation part of our site https://www.nova-ideo.com/documentation.

We can adapt Nova-Ideo to your specific needs. Do not hesitate to contact us. We will answer your questions!

You can also send us your observations and propose evolutions for the software, by creating an account on https://evolutions.nova-ideo.com

With kind regards.

The Ecréall team
Services and Solutions in Free, Libre and Open Source Software
Parc scientifique de la Haute Borne
Bâtiment Hub Innovation
11, rue de l'Harmonie
59650 Villeneuve d'Ascq
France
site : http://www.ecreall.com
tél : +33 (0)3 20 79 32 90
mob : +33 (0)6 16 85 91 12
Fax : +33 (0)9 56 94 39 44
"""


INVITATION_SUBJECT = u"""Invitation to join the {novaideo_title} participatory platform"""

INVITATION_MESSAGE = u"""
Dear,

{recipient_first_name} your are invited to join the the {novaideo_title} participatory platform as {roles}.

In order to validate your invitation, you must click on the following link {invitation_url} and follow the instructions.

""" + PORTAL_SIGNATURE

PRESENTATION_IDEA_SUBJECT = u"""Presentation of the idea "{subject_title}"""


PRESENTATION_IDEA_MESSAGE = u"""
Dear,

{my_first_name} {my_last_name} wishes to present to you the idea "{subject_title}" on the {novaideo_title} platform. You can access this idea at: {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE


CONFIRMATION_SUBJECT = u"""Confirmation of your registration on the {novaideo_title} participatory platform"""

CONFIRMATION_MESSAGE = u"""
Welcome on the {novaideo_title} platform!

We confirm hereby that you are registered on the {novaideo_title} participatory platform.

Share your ideas with us by connecting to the {login_url} address!

""" + PORTAL_SIGNATURE

PRESENTATION_PROPOSAL_SUBJECT = u"""Presentation of the proposal "{subject_title}""" 


PRESENTATION_PROPOSAL_MESSAGE = u"""
Dear,

{my_first_name} {my_last_name} wishes to present to you the proposal "{subject_title}" on the {novaideo_title} platform. You can access this proposal at: {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE

PRESENTATION_AMENDMENT_MESSAGE = u"""
Dear,

{my_first_name} {my_last_name} wishes to present to you the amendment "{subject_title}" on the {novaideo_title} platform. You can access this amendment at: {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE


PRESENTATION_AMENDMENT_SUBJECT = u"""« {subject_title} »"""


PRESENTATION_QUESTION_SUBJECT = u"""Presentation of the question "{subject_title}"""


PRESENTATION_QUESTION_MESSAGE = u"""
Dear,

{my_first_name} {my_last_name} wishes to present to you the question "{subject_title}" on the {novaideo_title} platform. You can access this question at: {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE

PRESENTATION_ANSWER_SUBJECT = u"""Presentation of an answer to the question "{subject_title}"""


PRESENTATION_ANSWER_MESSAGE = u"""
Dear,

{my_first_name} {my_last_name} wishes to present to you an answer to the question "{subject_title}" on the {novaideo_title} platform. You can access this answer at: {subject_url}.

""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE

AMENDABLE_FIRST_SUBJECT = u"""Start of the improvement cycle of the proposal "{subject_title}"""

AMENDABLE_FIRST_MESSAGE = u"""
Dear {recipient_first_name},

You are now three participants in the working group on the proposal "{subject_title}", which is accessible at {subject_url}. You can start improving it.

Each participant can suggest improvements, which the other participants can either accept, or refuse. Once the improvement cycle is finished, all participants vote, either to continue improving the proposal, or to submit it to the assessment of the members of the platform.

The improvement cycle ends on {duration}.

""" + PORTAL_SIGNATURE

AMENDABLE_SUBJECT = u"""Start of the improvement cycle of the proposal "{subject_title}"""


AMENDABLE_MESSAGE = u"""
Dear {recipient_first_name},

The working group on the proposal "{subject_title}", which is accessible at {subject_url}, voted in majority to continue improving it.

Each participant can suggest improvements, which the other participants can either accept, or refuse. Once the improvement cycle is finished, all participants vote, either to continue improving the proposal, or to submit it to the assessment of the members of the platform.

The improvement cycle ends on {duration}.

""" + PORTAL_SIGNATURE

ALERT_SUBJECT = u"""End of the improvement cycle of the proposal "{subject_title}" with no improvemt"""

ALERT_MESSAGE = u"""
Dear {recipient_first_name},

While the improvement cycle is finished, no improvement was brought to the proposal "{subject_title}", which can be accessed at {subject_url}. You will need to vote on whether you want to submit the proposal as it is, or to start again a new improvement cycle.

""" + PORTAL_SIGNATURE

ALERT_END_SUBJECT = u"""Last improvements before the end of the end of the improvement cycle of the proposal "{subject_title}"""

ALERT_END_MESSAGE = u"""
Dear {recipient_first_name},

The improvement cycle of the proposal "{subject_title}", which can be accessed at {subject_url}, is almost to an end. You can still improve it, before the working group votes to submit the proposal as it is or to start again a new improvement cycle.

""" + PORTAL_SIGNATURE

RESULT_VOTE_AMENDMENT_SUBJECT = u"""The results of the vote on the amendements related to the proposal "{subject_title}" """

RESULT_VOTE_AMENDMENT_MESSAGE = u"""
<div>
Dear {recipient_first_name},

{message_result}
</div>
""" + PORTAL_SIGNATURE

PUBLISHPROPOSAL_SUBJECT = u"""Decision to submit the proposal "{subject_title}" to the assessment of the members of the platform"""

PUBLISHPROPOSAL_MESSAGE = u"""
Dear {recipient_first_name},

The working group on the proposal "{subject_title}", which can be accessed at {subject_url}, voted in majority to submit the proposal to the assessment of the other members of the platform.

Every member of the platform can now suppport or oppose the proposal and the Examination Committee can evaluate it.

""" + PORTAL_SIGNATURE

SYSTEM_CLOSE_PROPOSAL_SUBJECT = u"""Decision to close the proposal "{subject_title}"""

SYSTEM_CLOSE_PROPOSAL_MESSAGE = u"""
Dear {recipient_first_name},

The working group on the proposal "{subject_title}", which can be accessed at {subject_url}, has not been active over several cycles, each lasting more than a week.

For this reason, the working group has been dissolved, and the proposal is now back to the stage "expecting the working group to reach the quorum".

""" + PORTAL_SIGNATURE

VOTINGPUBLICATION_SUBJECT = u"""Start of the vote to improve the proposal "{subject_title}" or to submit it to the assessment of the members of the platform"""

VOTINGPUBLICATION_MESSAGE = u"""
Dear {recipient_first_name},

The improvement cycle of the proposal "{subject_title}", which can be accessed at {subject_url}, is now finished. You are invited to participate in the vote to decide whether the proposal should be further improved, or whether it should be submitted to the assessment of the members of the platform.

You have 24 hours to vote. After this period of time, the ballots will be counted, and the outcome will be decided by the majority of expressed votes. If no ballot is cast, a new improvement cycle starts for one week.

""" + PORTAL_SIGNATURE

VOTINGAMENDMENTS_SUBJECT = u"""Start of the votes on the amendments to the proposal "{subject_title}"""

VOTINGAMENDMENTS_MESSAGE = u"""
Dear {recipient_first_name},

The votes on the amendments to the proposal "{subject_title}", which can be accessed at {subject_url}, have started. You are kindly requested to  participate in the votes.

""" + PORTAL_SIGNATURE

WITHDRAW_SUBJECT = u"""Withdrawal from the waiting list of the working group related to the proposal "{subject_title}"""

WITHDRAW_MESSAGE = u"""
Dear {recipient_first_name},

You are not any more on the waiting list of the working group related to the proposal {subject_title}, which can be accessed at {subject_url}, following your decision to withdraw from this waiting list.

You can attempt at any time to join again the working group related to the proposal, if it still is being improved.

""" + PORTAL_SIGNATURE

PARTICIPATE_WL_SUBJECT = u"""Participation in the working group related to the proposal "{subject_title}"""

PARTICIPATE_WL_MESSAGE = u"""
Dear {recipient_first_name},

A participant has left the working group related to the proposal {subject_title}, which can be accessed at {subject_url}. His/her departure has opened a free place for you in the working group. You are now part of the working group related to the proposal {subject_title}.

As a participant in the working group, you can improve the proposal, and at the end of the improvement cycle, vote on whether to continue improving it or to submit it to the assessment of the members of the platform.

""" + PORTAL_SIGNATURE

PARTICIPATE_SUBJECT = u"""Your participation in the working group related to the proposal "{subject_title}"""

PARTICIPATE_MESSAGE = u"""
Dear {recipient_first_name},

You are part of the working group related to the proposal {subject_title}, which can be accessed at {subject_url}.

As a participant in the working group, you can improve the proposal, and at the end of the improvement cycle, vote on whether to continue improving it or to submit it to the assessment of the members of the platform.

""" + PORTAL_SIGNATURE

RESIGN_SUBJECT = u"""Your departure from the working group related to the proposal "{subject_title}"""

RESIGN_MESSAGE = u"""
Dear {recipient_first_name},

We hereby confirm that you are not any more  participant in the working group related to the proposal "{subject_title}", which can be accessed at {subject_url}.

You will be able to join it again at any time, if you are not already a participant in five working groups, which is the maximum number of working groups in which a member can simultaneously participate at any time.

""" + PORTAL_SIGNATURE

WATINGLIST_SUBJECT = u"""Registration in the waiting list of the working group related to the proposal "{subject_title}"""

WATINGLIST_MESSAGE = u"""
Dear {recipient_first_name},

You wish to participate in the working group related to the proposal "{subject_title}", which can be accessed at {subject_url}. However, the number of participants has already reached 12, which is the maximum number of participants in a working group.

You are therefore on the waiting list of this working group, and will automatically become a participant in it, as soon as a place is free.

""" + PORTAL_SIGNATURE

NEWCONTENT_SUBJECT = u"""{subject_type} "{subject_title}", which contains a keyword among your topics of interest, has just been published."""

NEWCONTENT_MESSAGE = u"""
Dear {recipient_first_name},

{subject_type} "{subject_title}", which contains a keyword among your topics of interest, has just been published. You can access it at the following URL {subject_url}.

""" + PORTAL_SIGNATURE

CONTENTMODIFIEF_SUBJECT = u"""{subject_type} "subject_title}", which is among your favourites, has changed its status"""

CONTENTMODIFIEF_MESSAGE = u"""
Dear {recipient_first_name},

{subject_type} "subject_title}", which is among your favourites, has just switched from the status {state_source} to the status {state_target}. You can access it at the following URL {subject_url}.

""" + PORTAL_SIGNATURE

ARCHIVEIDEA_SUBJECT = u"""Decision by the moderators to archive the idea "{subject_title}"""

ARCHIVEIDEA_MESSAGE = u"""
Dear {recipient_first_name},

The idea "{subject_title}" has just been archived by the moderators, for the following reason:

{explanation}

You can access your idea at the following URL {subject_url}.

""" + PORTAL_SIGNATURE

ARCHIVECONTENT_SUBJECT = u"""Decision by the moderators to archive the content "{subject_title}"""


ARCHIVECONTENT_MESSAGE = u"""
Dear {recipient_first_name},

The content "{subject_title}" has just been archived by the moderators, for the following reason:

{explanation}

You can access your content at the following URL {subject_url}.

""" + PORTAL_SIGNATURE

ARCHIVEPROPOSAL_SUBJECT = u"""Decision by the moderators to archive the proposal "{subject_title}"""

ARCHIVEPROPOSAL_MESSAGE = u"""
Dear {recipient_first_name},

The proposal "{subject_title}" has just been archived by the moderators, for the following reason:

{explanation}

You can access your proposal at the following URL {subject_url}.

""" + PORTAL_SIGNATURE

ALERTOPINION_SUBJECT = u"""Opinion of the Examination Committee on the proposal "{subject_title}"""

ALERTOPINION_MESSAGE = u"""
Dear {recipient_first_name},

The Examination Committee has expressed the following opinion "{opinion}" on the proposal "{subject_title}", with the following explanation:  "{explanation}".

""" + PORTAL_SIGNATURE

ALERTOPINIONIDEA_SUBJECT = u"""Opinion of an Examiner on the idea "{subject_title}"""

ALERTOPINIONIDEA_MESSAGE = u"""
Dear {recipient_first_name},

An Examiner has expressed the following opinion "{opinion}" on the idea "{subject_title}", with the following explanation:  "{explanation}".

""" + PORTAL_SIGNATURE

PUBLISHEDIDEA_SUBJECT = u"""Decision by the moderators to publish the idea "{subject_title}"""

PUBLISHEDIDEA_MESSAGE = u"""
Dear {recipient_first_name},

The idea "{subject_title}", which is accessible at the URL {subject_url}, has just been published by the moderators. This idea can now be used by any member of the platform to build a proposal.

""" + PORTAL_SIGNATURE

PUBLISHEDPROPOSAL_SUBJECT = u"""Decision by the moderators to publish the proposal "{subject_title}"""

PUBLISHEDPROPOSAL_MESSAGE = u"""
Dear {recipient_first_name},

The proposal "{subject_title}", which can be accessed at {subject_url}, has just been published by the moderators. The working group is created, and is waiting to reach the quorum.

""" + PORTAL_SIGNATURE

PROPOSALREMOVED_SUBJECT = u"""Suppression of proposal "{subject_title}"""

PROPOSALREMOVED_MESSAGE = u"""
Dear {recipient_first_name},

The proposal "{subject_title}" has just been suppressed by the moderators for the following reason:

« {explanation} »

""" + PORTAL_SIGNATURE

REFUSE_INVITATION_SUBJECT = u"""{user_first_name} {user_last_name} has refused to join the platform {novaideo_title}"""

REFUSE_INVITATION_MESSAGE = u"""
Dear,

We inform you that {user_first_name} {user_last_name} has refused your invitation to join the platform {novaideo_title}.

""" + PORTAL_SIGNATURE

ACCEPT_INVITATION_SUBJECT = u"""{user_first_name} {user_last_name} has accepted to join the platform {novaideo_title}"""

ACCEPT_INVITATION_MESSAGE = u"""
Dear {recipient_first_name},

We inform you that {user_first_name} {user_last_name} has accepted your invitation to join the platform {novaideo_title}.

""" + PORTAL_SIGNATURE

RESETPW_SUBJECT = u"""Your new password on the platform {novaideo_title}"""

RESETPW_MESSAGE = u"""
Dear {recipient_first_name},

You have asked for a new password on the platform {novaideo_title}. Please click on the following URL {reseturl} and provide your new password.

""" + PORTAL_SIGNATURE

PREREGISTRATION_SUBJECT = u"""Finalise your registration on the {novaideo_title} participatory platform"""

PREREGISTRATION_MESSAGE = u"""
Dear {recipient_first_name},

You have registered on the {novaideo_title} participatory platform.

In order to finalise your registration, you must now click on the following link {url}. This link is valid for 48 hours. You must therefore complete your registration on or before {deadline_date}.

We are happy to count you among our members. We hope that your participation will be for you a positive and rewarding experience, in a fully democractic framework. Welcome!

"""+ PORTAL_SIGNATURE

ADMIN_PREREGISTRATION_SUBJECT = u"""Registration on the participatory platform {novaideo_title}"""

ADMIN_PREREGISTRATION_MESSAGE = u"""
Dear {recipient_first_name},

A new registration on the participatory platform {novaideo_title} has been recorded. It can be visualised at the following URL {url}. As a moderator, you must decide on whether or not you want to accept it.

""" + PORTAL_SIGNATURE

ALERTCOMMENT_SUBJECT = u"""New comment on {subject_type} "{subject_title}"""

ALERTCOMMENT_MESSAGE = u"""
Dear {recipient_first_name},

A new comment has been added on the {subject_type} "{subject_title}".

"{comment_content}"

You can access it at the following URL {comment_url} and answer it.

""" + PORTAL_SIGNATURE

ALERTANSWER_SUBJECT = u"""New answer given to {subject_type} "{subject_title}"""

ALERTANSWER_MESSAGE = u"""
Dear {recipient_first_name},

A new answer was given to {subject_type} "{subject_title}".

"{comment_content}"

You can access it at the following URL {comment_url} and answer it.

""" + PORTAL_SIGNATURE

ALERTDISCUSS_SUBJECT = u"""New message added to your discussion with "subject_title}"""

ALERTDISCUSS_MESSAGE = u"""
Dear {recipient_first_name},

A new message has been added to your discussion with "{subject_title}".

"{comment_content}"

You can access it at the following URL {comment_url} and answer it.

""" + PORTAL_SIGNATURE

ALERTRESPONS_SUBJECT = u"""A person has given an answer to a comment on the {subject_type} "{subject_title}"""

ALERTRESPONS_MESSAGE = u"""
Dear {recipient_first_name},

A person has given an answer to a comment on the {subject_type} "{subject_title}, which can be accessed at the following URL{comment_url}.

"{comment_content}"

""" + PORTAL_SIGNATURE

NEWSLETTER_SUBSCRIPTION_SUBJECT = u"""Subscription to the newsletter"""

NEWSLETTER_SUBSCRIPTION_MESSAGE = u"""
Dear {first_name} {last_name},

Your subscription to the newsletter {newsletter_title} is now confirmed.

""" + PORTAL_SIGNATURE

NEWSLETTER_UNSUBSCRIPTION_SUBJECT = u"""Unsubscription from the newsletter"""

NEWSLETTER_UNSUBSCRIPTION_MESSAGE = u"""
Dear {first_name} {last_name},

Your subscription to the newsletter {newsletter_title} is now cancelled.

""" + PORTAL_SIGNATURE

PUBLISHEDCHALLENGE_SUBJECT = u"""Decision by the moderators to publish the challenge "{subject_title}"""

PUBLISHEDCHALLENGE_MESSAGE = u"""
Dear {recipient_first_name},

The challenge "{subject_title}", which can be accessed at {subject_url}, has just been published by the moderators.

""" + PORTAL_SIGNATURE

ARCHIVECHALLENGE_SUBJECT = u"""Decision by the moderators to archive the challenge "{subject_title}"""

ARCHIVECHALLENGE_MESSAGE = u"""
Dear {recipient_first_name},

The challenge "{subject_title}" has just been archived by the moderators, for the following reason:

{explanation}

You can access your challenge at the following URL {subject_url}.

""" + PORTAL_SIGNATURE

PRESENTATION_CHALLENGE_SUBJECT = u"""Presentation of the challenge "{subject_title}""" 

PRESENTATION_CHALLENGE_MESSAGE = u"""
Dear,

{my_first_name} {my_last_name} wishes to present to you the challenge "{subject_title}" on the {novaideo_title} platform. You can access this challenge at: {subject_url}.
""" + PORTAL_PRESENTATION + PORTAL_SIGNATURE

FIRST_INVITATION = {
    'subject': FIRST_INVITATION_SUBJECT,
    'template': FIRST_INVITATION_MESSAGE
}

mail_locale = 'en'

add_mail_template('invitation', {'locale': mail_locale,
                   'subject': INVITATION_SUBJECT,
                   'template': INVITATION_MESSAGE})

add_mail_template('refuse_invitation', {'locale': mail_locale,
                   'subject': REFUSE_INVITATION_SUBJECT,
                   'template': REFUSE_INVITATION_MESSAGE})

add_mail_template('accept_invitation', {'locale': mail_locale,
                   'subject': ACCEPT_INVITATION_SUBJECT,
                   'template': ACCEPT_INVITATION_MESSAGE})

add_mail_template('reset_password', {'locale': mail_locale,
                   'subject': RESETPW_SUBJECT,
                   'template': RESETPW_MESSAGE})

add_mail_template('registration_confiramtion', {'locale': mail_locale,
                   'subject': CONFIRMATION_SUBJECT,
                   'template': CONFIRMATION_MESSAGE})

add_mail_template('preregistration', {'locale': mail_locale,
                   'subject': PREREGISTRATION_SUBJECT,
                   'template': PREREGISTRATION_MESSAGE})


add_mail_template('presentation_idea', {'locale': mail_locale,
                    'subject': PRESENTATION_IDEA_SUBJECT,
                   'template': PRESENTATION_IDEA_MESSAGE})


add_mail_template('presentation_proposal', {'locale': mail_locale,
                   'subject': PRESENTATION_PROPOSAL_SUBJECT,
                   'template': PRESENTATION_PROPOSAL_MESSAGE})

add_mail_template('presentation_amendment', {'locale': mail_locale,
                   'subject': PRESENTATION_AMENDMENT_SUBJECT,
                   'template': PRESENTATION_AMENDMENT_MESSAGE})

add_mail_template('first_start_work', {'locale': mail_locale,
                   'subject': AMENDABLE_FIRST_SUBJECT,
                   'template': AMENDABLE_FIRST_MESSAGE})

add_mail_template('start_work', {'locale': mail_locale,
                   'subject': AMENDABLE_SUBJECT,
                   'template': AMENDABLE_MESSAGE})

add_mail_template('alert_amendment', {'locale': mail_locale,
                   'subject': ALERT_SUBJECT,
                   'template': ALERT_MESSAGE})

add_mail_template('alert_end', {'locale': mail_locale,
                   'subject': ALERT_END_SUBJECT,
                   'template': ALERT_END_MESSAGE})

add_mail_template('vote_amendment_result', {'locale': mail_locale,
                   'subject': RESULT_VOTE_AMENDMENT_SUBJECT,
                   'template': RESULT_VOTE_AMENDMENT_MESSAGE})

add_mail_template('publish_proposal', {'locale': mail_locale,
                    'subject': PUBLISHPROPOSAL_SUBJECT,
                   'template': PUBLISHPROPOSAL_MESSAGE})

add_mail_template('start_vote_publishing', {'locale': mail_locale,
                   'subject': VOTINGPUBLICATION_SUBJECT,
                   'template': VOTINGPUBLICATION_MESSAGE})

add_mail_template('start_vote_amendments', {'locale': mail_locale,
                   'subject': VOTINGAMENDMENTS_SUBJECT,
                   'template': VOTINGAMENDMENTS_MESSAGE})

add_mail_template('withdeaw', {'locale': mail_locale,
                   'subject': WITHDRAW_SUBJECT,
                   'template': WITHDRAW_MESSAGE})

add_mail_template('wg_wating_list_participation', {'locale': mail_locale,
                   'subject': PARTICIPATE_WL_SUBJECT,
                   'template': PARTICIPATE_WL_MESSAGE})

add_mail_template('wg_participation', {'locale': mail_locale,
                   'subject': PARTICIPATE_SUBJECT,
                   'template': PARTICIPATE_MESSAGE})

add_mail_template('wg_resign', {'locale': mail_locale,
                   'subject': RESIGN_SUBJECT,
                  'template': RESIGN_MESSAGE})

add_mail_template('wating_list', {'locale': mail_locale,
                  'subject': WATINGLIST_SUBJECT,
                  'template': WATINGLIST_MESSAGE})

add_mail_template('alert_new_content', {'locale': mail_locale,
                  'subject': NEWCONTENT_SUBJECT,
                  'template': NEWCONTENT_MESSAGE})

add_mail_template('alert_content_modified', {'locale': mail_locale,
                  'subject': CONTENTMODIFIEF_SUBJECT,
                  'template': CONTENTMODIFIEF_MESSAGE})

add_mail_template('archive_idea_decision', {'locale': mail_locale,
                  'subject': ARCHIVEIDEA_SUBJECT,
                  'template': ARCHIVEIDEA_MESSAGE})

add_mail_template('opinion_proposal', {'locale': mail_locale,
                  'subject': ALERTOPINION_SUBJECT,
                  'template': ALERTOPINION_MESSAGE})

add_mail_template('opinion_idea', {'locale': mail_locale,
                  'subject': ALERTOPINIONIDEA_SUBJECT,
                  'template': ALERTOPINIONIDEA_MESSAGE})

add_mail_template('publish_idea_decision', {'locale': mail_locale,
                  'subject': PUBLISHEDIDEA_SUBJECT,
                  'template': PUBLISHEDIDEA_MESSAGE})

add_mail_template('archive_proposal_decision', {'locale': mail_locale,
                  'subject': ARCHIVEPROPOSAL_SUBJECT,
                  'template': ARCHIVEPROPOSAL_MESSAGE})

add_mail_template('publish_proposal_decision', {'locale': mail_locale,
                  'subject': PUBLISHEDPROPOSAL_SUBJECT,
                  'template': PUBLISHEDPROPOSAL_MESSAGE})

add_mail_template('delete_proposal', {'locale': mail_locale,
                  'subject': PROPOSALREMOVED_SUBJECT,
                  'template': PROPOSALREMOVED_MESSAGE})

add_mail_template('alert_comment', {'locale': mail_locale,
                  'subject': ALERTCOMMENT_SUBJECT,
                  'template': ALERTCOMMENT_MESSAGE})

add_mail_template('alert_discuss', {'locale': mail_locale,
                   'subject': ALERTDISCUSS_SUBJECT,
                   'template': ALERTDISCUSS_MESSAGE})

add_mail_template('alert_respons', {'locale': mail_locale,
                   'subject': ALERTRESPONS_SUBJECT,
                   'template': ALERTRESPONS_MESSAGE})

add_mail_template('newsletter_subscription', {'locale': mail_locale,
                   'subject': NEWSLETTER_SUBSCRIPTION_SUBJECT,
                        'template': NEWSLETTER_SUBSCRIPTION_MESSAGE})

add_mail_template('newsletter_unsubscription', {'locale': mail_locale,
                   'subject': NEWSLETTER_UNSUBSCRIPTION_SUBJECT,
                   'template': NEWSLETTER_UNSUBSCRIPTION_MESSAGE})

add_mail_template('moderate_preregistration', {'locale': mail_locale,
                   'subject': ADMIN_PREREGISTRATION_SUBJECT,
                   'template': ADMIN_PREREGISTRATION_MESSAGE})

add_mail_template('close_proposal', {'locale': mail_locale,
                    'subject': SYSTEM_CLOSE_PROPOSAL_SUBJECT,
                   'template': SYSTEM_CLOSE_PROPOSAL_MESSAGE})


add_mail_template('presentation_question', {'locale': mail_locale,
                   'subject': PRESENTATION_QUESTION_SUBJECT,
                   'template': PRESENTATION_QUESTION_MESSAGE})

add_mail_template('presentation_answer', {'locale': mail_locale,
                   'subject': PRESENTATION_ANSWER_SUBJECT,
                   'template': PRESENTATION_ANSWER_MESSAGE})

add_mail_template('alert_answer', {'locale': mail_locale,
                   'subject': ALERTANSWER_SUBJECT,
                   'template': ALERTANSWER_MESSAGE})

add_mail_template('archive_content_decision', {'locale': mail_locale,
                   'subject': ARCHIVECONTENT_SUBJECT,
                   'template': ARCHIVECONTENT_MESSAGE})

add_mail_template('archive_challenge_decision', {'locale': mail_locale,
                   'subject': ARCHIVECHALLENGE_SUBJECT,
                   'template': ARCHIVECHALLENGE_MESSAGE})

add_mail_template('publish_challenge_decision', {'locale': mail_locale,
                   'subject': PUBLISHEDCHALLENGE_SUBJECT,
                   'template': PUBLISHEDCHALLENGE_MESSAGE})

add_mail_template('presentation_challenge', {'locale': mail_locale,
             'subject': PRESENTATION_CHALLENGE_SUBJECT,
             'template': PRESENTATION_CHALLENGE_MESSAGE})
