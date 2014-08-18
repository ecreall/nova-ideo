# -*- coding: utf8 -*-
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import  Associate
from novaideo.content.correlation import CorrelationSchema, Correlation
from novaideo.content.idea import Idea
from novaideo import _
from .add_to_proposals import targets_choice


class RelatedContentsView(BasicView):
    title = _('Related contents')
    name = 'relatedcontents'
    template = 'novaideo:views/idea_management/templates/related_contents.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'relatedcontents'


    def update(self):
        user = get_current()
        correlations = [c for c in self.context.source_correlations if c.type==0]# TODO (if c.source.actions) replace by an other test
        target_correlations = [c for c in self.context.target_correlations if c.type==0]# TODO (if c.target.actions) replace by an other test
        relatedcontents = []
        for c in correlations:
            contents = c.targets
            for content in contents:
                relatedcontents.append({'content':content, 'url':content.url(self.request), 'correlation': c})

        for c in target_correlations:
            content = c.source
            relatedcontents.append({'content':content, 'url':content.url(self.request), 'correlation': c})

        len_contents = len(relatedcontents)
        message = ''
        if len_contents>1:
            message = u"""Voir les {len} contenus associés""".format(len=len_contents)
        elif len_contents == 0:
            message = u"""Pas de contenus associés"""
        else:   
            message = u"""Voir le contenu associé"""


        result = {}
        values = {
                'relatedcontents': relatedcontents,
                'current_user': user,
                'message': message
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class AssociateFormView(FormView):

    title = _('Associate')
    schema = select(CorrelationSchema(factory=Correlation, editable=True),['targets', 'intention','comment'])
    behaviors = [Associate]
    formid = 'formassociate'
    name='associateform'

    def before_update(self):
        target = self.schema.get('targets')
        target.title = _("Related contents")


@view_config(
    name='associate',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class AssociateView(MultipleView):
    title = _('Associate')
    name = 'associate'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (AssociateFormView, RelatedContentsView)



DEFAULTMAPPING_ACTIONS_VIEWS.update({Associate:AssociateView})
