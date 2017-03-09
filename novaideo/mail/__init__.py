# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from novaideo import _

""" The contents of e-mails"""

DEFAULT_SITE_MAILS = {
    'invitation': {
        'title': _("Invitation"),
        'languages': {}
    },
    'refuse_invitation': {
        'title': _("Refuse the invitation"),
        'languages': {}
    },
    'accept_invitation': {
        'title': _("Accept the invitation"),
        'languages': {}
    },
    'reset_password': {
        'title': _("Reset the password"),
        'languages': {}
    },
    'registration_confiramtion': {
        'title': _("Registration confirmation"),
        'languages': {}
    },
    'preregistration': {
        'title': _("Pre-registration of users"),
        'languages': {}
    },

    'presentation_idea': {
        'title': _("Presentation of an idea"),
        'languages': {}
    },

    'presentation_proposal': {
        'title': _("Presentation of a proposal"),
        'languages': {}
    },
    'presentation_amendment': {
        'title': _('Presentation of an amendment'),
        'languages': {}
    },
    'first_start_work': {
        'title': _('Start of the improvement cycle'),
        'languages': {}
    },
    'start_work': {
        'title': _('Start of the improvement cycle'),
        'languages': {}
    },
    'alert_amendment': {
        'title': _("Inactivity alert"),
        'languages': {}
    },
    'alert_end': {
        'title': _("End of the improvement cycle"),
        'languages': {}
    },
    'vote_amendment_result': {
        'title': _("Result of the ballot (amendments)"),
        'languages': {}
    },
    'publish_proposal': {
        'title': _("Publication of the proposal"),
        'languages': {}
    },
    'start_vote_publishing': {
        'title': _("Start of the ballot (publication of the proposal)"),
        'languages': {}
    },
    'start_vote_amendments': {
        'title': _("Start of the ballot (amendments)"),
        'languages': {}
    },
    'withdeaw': {
        'title': _("Withdraw"),
        'languages': {}
    },
    'wg_wating_list_participation': {
        'title': _("Automatic addition of a participant in the working group that was on the waiting list"),
        'languages': {}
    },
    'wg_participation': {
        'title': _("Participation in the working group"),
        'languages': {}
    },
    'wg_resign': {
        'title': _("Resignation from the working group"),
        'languages': {}
    },
    'wating_list': {
        'title': _("Registration on the waiting list"),
        'languages': {}
    },
    'alert_new_content': {
        'title': _("Alert (new content)"),
        'languages': {}
    },
    'alert_content_modified': {
        'title': _("Alert (content modified)"),
        'languages': {}
    },
    'archive_idea_decision': {
        'title': _("Moderation: Archive the idea"),
        'languages': {}
    },
    'opinion_proposal': {
        'title': _("Moderation: Opinion on the proposal"),
        'languages': {}
    },
    'opinion_idea': {
        'title': _("Moderation: Opinion on the idea"),
        'languages': {}
    },
    'publish_idea_decision': {
        'title': _("Moderation: Publish the idea"),
        'languages': {}
    },
    'archive_proposal_decision': {
        'title': _("Moderation: Archive the proposal"),
        'languages': {}
    },
    'publish_proposal_decision': {
        'title': _("Moderation: Publish the proposal"),
        'languages': {}
    },
    'delete_proposal': {
        'title': _("Moderation: Delete the proposal"),
        'languages': {}
    },
    'alert_comment': {
        'title': _("Warning: new comment"),
        'languages': {}
    },
    'alert_discuss': {
        'title': _("Warning: new discussion"),
        'languages': {}
    },
    'alert_respons': {
        'title': _("Alert: answer"),
        'languages': {}
    },
    'newsletter_subscription': {
        'title': _("Subscription to the newsletter"),
        'languages': {}
    },
    'newsletter_unsubscription': {
        'title': _("Unsubscription from the newsletter"),
        'languages': {}
    },
    'moderate_preregistration': {
        'title': _("New registration"),
        'languages': {}
    },
    'close_proposal': {
        'title': _("Close the proposal"),
        'languages': {}
    },

    'presentation_question': {
        'title': _("Presentation of a question"),
        'languages': {}
    },

    'presentation_answer': {
        'title': _("Presentation of an answer"),
        'languages': {}
    },
    'alert_answer': {
        'title': _("Warning: new answer"),
        'languages': {}
    },
    'archive_content_decision': {
        'title': _("Moderation: Archive the content"),
        'languages': {}
    },
    'archive_challenge_decision': {
        'title': _("Moderation: Archive the challenge"),
        'languages': {}
    },
    'publish_challenge_decision': {
        'title': _("Moderation: Publish the challenge"),
        'languages': {}
    },

    'presentation_challenge': {
        'title': _("Presentation of a challenge"),
        'languages': {}
    }
}


def add_mail_template(mail_id, template):
    locale = template.get('locale', None)
    if locale:
        mail = DEFAULT_SITE_MAILS.get(mail_id, None)
        if mail:
            mail.get('languages')[locale] = template
