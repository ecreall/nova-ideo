# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid import renderers
from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.default_behavior import Cancel
from pontus.view_operation import MultipleView
from pontus.widget import Select2Widget

from novaideo.content.processes.proposal_management.behaviors import (
    PublishAsProposal)
from novaideo.content.idea import Idea
from .create_proposal import (
    CreateProposalFormView,
    CreateProposalView,
    AddIdeaFormView,
    add_file_data,
    IdeaManagementView as IdeaManagementViewOr)
from novaideo import _



class RelatedIdeasView(BasicView):
    title = _('Related Ideas')
    name = 'relatedideas'
    template = 'novaideo:views/proposal_management/templates/ideas_management.pt'
    idea_template = 'novaideo:views/proposal_management/templates/idea_data.pt'
    viewid = 'relatedideas'
    coordinates = 'right'

    def update(self):
        result = {}
        target = None
        try:
            editform = self.parent.parent.validated_children[0].validated_children[1]
            target = editform.viewid+'_'+editform.formid 
        except Exception:
            pass


        ideas = [{'title': self.context.title,
                'id': get_oid(self.context),
                'body': renderers.render(self.idea_template, 
                                         {'idea':self.context}, self.request)
                }]
        values = {
                'items': ideas,
                'target' : target
               }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class IdeaManagementView(IdeaManagementViewOr):
    views = (RelatedIdeasView, AddIdeaFormView)


class PublishAsProposalStudyReport(BasicView):
    title = _('Alert for transformation')
    name = 'alertfortransformation'
    template ='novaideo:views/proposal_management/templates/alert_proposal_transformation.pt'

    def update(self):
        result = {}
        body = self.content(args={}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


def ideas_choice(context, request):   
    values = [(context, context.title)]
    return Select2Widget(values=values, multiple=True)


class PublishFormView(CreateProposalFormView):
    title = _('Transform the idea into a proposal')
    formid = 'formpublishasproposal'
    behaviors = [PublishAsProposal, Cancel]
    name = 'publishasproposal'

    def default_data(self):
        localizer = self.request.localizer
        title = self.context.title + \
                    localizer.translate(_(" (the proposal)"))
        data = {'title': title,
                'text': self.context.text,
                'keywords': self.context.keywords,
                'related_ideas': [self.context]}
        attached_files = self.context.attached_files
        data['add_files'] = {'attached_files': []}
        files = []
        for file_ in attached_files:
            file_data = add_file_data(file_)
            if file_data:
                files.append(file_data)

        if files:
            data['add_files']['attached_files'] = files

        return data

    def before_update(self):
        ideas_widget = ideas_choice(self.context, self.request)
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget


class PublishAsProposalFormView(MultipleView):
    title = _('Transform the idea into a proposal')
    name = 'publishasproposalview'
    viewid = 'publishasproposalview'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    views = (PublishAsProposalStudyReport, PublishFormView)


@view_config(
    name='publishasproposal',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishAsProposalView(CreateProposalView):
    title = _('Transform the idea into a proposal')
    name = 'publishasproposal'
    viewid = 'publishasproposal'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    views = (PublishAsProposalFormView, IdeaManagementView)
    validators = [PublishAsProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({PublishAsProposal:PublishAsProposalView})
