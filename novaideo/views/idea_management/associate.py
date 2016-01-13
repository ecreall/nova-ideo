# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.util import merge_dicts
from daceui.interfaces import IDaceUIAPI

from novaideo.content.processes.idea_management.behaviors import  Associate
from novaideo.content.correlation import CorrelationSchema, Correlation
from novaideo.content.idea import Idea
from novaideo import _
from novaideo.core import can_access


ASSOCIATION_MESSAGES = {'0': _(u"""Pas de contenus associés"""),
                        '1': _(u"""Contenu associé"""),
                        '*': _(u"""Contenus associés""")}


class RelatedContentsView(BasicView):
    title = _('Related contents')
    name = 'relatedcontents'
    template = 'novaideo:views/idea_management/templates/related_contents.pt'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'
    viewid = 'relatedcontents'

    def _correlation_action(self, correlation):
        dace_ui_api = get_current_registry().getUtility(
                                               IDaceUIAPI,'dace_ui_api')
        correlation_actions = dace_ui_api.get_actions([correlation], 
                                                      self.request, 
                                                      'correlationmanagement', 
                                                      'comment')
        correlation_action = {}
        action_updated, messages, \
        resources, actions = dace_ui_api.update_actions(
                                        self.request, correlation_actions)
        if actions: 
            correlation_action['correlationaction'] = actions[0]

        return correlation_action, resources, messages, action_updated

    def _update_data(self, messages, resources, all_messages, all_resources):
        all_messages.update(messages)
        if resources is not None:
            if 'js_links' in resources:
                all_resources['js_links'].extend(resources['js_links'])
                all_resources['js_links'] = list(set(all_resources['js_links']))

            if 'css_links' in resources:
                all_resources['css_links'].extend(resources['css_links'])
                all_resources['css_links'] = list(set(all_resources['css_links']))

    def update(self):
        user = get_current()
        correlations = [c for c in self.context.source_correlations \
                        if c.type == 0 and can_access(user, c)]
        target_correlations = [c for c in self.context.target_correlations \
                               if c.type == 0 and can_access(user, c)]
        relatedcontents = []
        all_messages = {}
        isactive = False
        all_resources = {}
        all_resources['js_links'] = []
        all_resources['css_links'] = []
        for correlation in correlations:
            contents = correlation.targets
            for content in contents:
                correlation_data, resources, \
                messages, action_updated = self._correlation_action(correlation)
                correlation_data.update({'content': content,
                                         'url': content.url,
                                         'correlation': correlation})
                relatedcontents.append(correlation_data)
                isactive = action_updated or isactive
                self._update_data(messages, resources,
                                  all_messages, all_resources)

        for correlation in target_correlations:
            content = correlation.source
            correlation_data, resources, \
            messages, action_updated = self._correlation_action(correlation)
            correlation_data.update({'content': content,
                                     'url': content.url,
                                     'correlation': correlation})
            relatedcontents.append(correlation_data)
            isactive = action_updated or isactive
            self._update_data(messages, resources, all_messages, all_resources)

        len_contents = len(relatedcontents)
        index = str(len_contents)
        if len_contents > 1:
            index = '*'

        message = (_(ASSOCIATION_MESSAGES[index]),
                  len_contents,
                  index)
        self.message = message
        result = {}
        values = {
                'relatedcontents': relatedcontents,
                'current_user': user,
                'message': message
               }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        item['messages'] = all_messages
        item['isactive'] = isactive
        result.update(all_resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result


class AssociateFormView(FormView):

    title = _('Associate contents')
    schema = select(CorrelationSchema(factory=Correlation, 
                                      editable=True),
                    ['targets', 'intention', 'comment'])
    behaviors = [Associate]
    formid = 'formassociate'
    name = 'associateform'


    def before_update(self):
        target = self.schema.get('targets')
        target.title = _("Related contents")
        formwidget = deform.widget.FormWidget(css_class='controled-form', 
                                activable=True,
                                button_css_class="pull-right",
                                picto_css_class="glyphicon glyphicon-link",
                                button_title=_("Associate contents"))
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='associate',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AssociateView(MultipleView):
    title = _('Associate the idea')
    name = 'associate'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (RelatedContentsView, AssociateFormView)
    description = _("Associate the idea to an other content")

    def get_message(self):
        message = (ASSOCIATION_MESSAGES['0']).format()
        if self.validated_children:
            message = getattr(self.validated_children[0], 'message', message)

        return message


DEFAULTMAPPING_ACTIONS_VIEWS.update({Associate:AssociateView})
