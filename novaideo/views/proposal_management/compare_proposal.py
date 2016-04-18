# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.proposal_management.behaviors import (
    CompareProposal)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.views.idea_management.compare_idea import (
    CompareIdeaFormView,
    CompareIdeaView,
    DiffView as DiffViewIdea)


class DiffView(DiffViewIdea):
    template = 'novaideo:views/proposal_management/templates/diff_result.pt'
    validators = [CompareProposal.get_validator()]


class CompareProposalFormView(CompareIdeaFormView):
    title = _('Compare proposal form')
    behaviors = [CompareProposal]
    formid = 'formcompareproposal'
    name = 'compareproposalform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='compareform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget
        view_name = 'compare'
        formwidget.ajax_url = self.request.resource_url(self.context,
                                                        '@@'+view_name)


@view_config(
    name='compare',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CompareProposalView(CompareIdeaView):
    title = _('Compare versions')
    name = 'compare'
    views = (CompareProposalFormView, DiffView)

    def before_update(self):
        self.viewid = 'compare'
        super(CompareProposalView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CompareProposal: CompareProposalView})
