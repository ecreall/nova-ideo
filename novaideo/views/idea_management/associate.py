# -*- coding: utf8 -*-
import deform
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from dace.util import getSite
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.idea_management.behaviors import  Associate
from novaideo.content.correlation import CorrelationSchema, Correlation
from novaideo.content.idea import Idea
from novaideo import _
from novaideo.core import can_access


associate_messages = {'0': _(u"""Pas de contenus asociés"""),
                      '1': _(u"""Un contenu asocié"""),
                      '*': _(u"""${lenassociated} contenus asociés""")}


class RelatedContentsView(BasicView):
    title = _('Related contents')
    name = 'relatedcontents'
    template = 'novaideo:views/idea_management/templates/related_contents.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'relatedcontents'

    def _correlation_action(self, correlation):
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        correlation_action = {}
        action_updated, messages, resources, actions = dace_ui_api._actions(self.request, correlation, 'correlationmanagement', 'comment')
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
                all_resources['css_links'] =list(set(all_resources['css_links']))


    def update(self):
        user = get_current()
        root = getSite()
        correlations = [c for c in self.context.source_correlations if c.type==0 and can_access(user, c, self.request, root)]
        target_correlations = [c for c in self.context.target_correlations if c.type==0 and can_access(user, c, self.request, root)]
        relatedcontents = []
        all_messages = {}
        isactive = False
        all_resources = {}
        all_resources['js_links'] = []
        all_resources['css_links'] = []
        for c in correlations:
            contents = c.targets
            for content in contents:
                correlation_data, resources, messages, action_updated =  self._correlation_action(c)
                correlation_data.update({'content':content, 'url':content.url(self.request), 'correlation': c})
                relatedcontents.append(correlation_data)
                isactive = action_updated or isactive
                self._update_data(messages, resources, all_messages, all_resources)

        for c in target_correlations:
            content = c.source
            correlation_data, resources, messages, action_updated =  self._correlation_action(c)
            correlation_data.update({'content':content, 'url':content.url(self.request), 'correlation': c})
            relatedcontents.append(correlation_data)
            isactive = action_updated or isactive
            self._update_data(messages, resources, all_messages, all_resources)

        len_contents = len(relatedcontents)
        index = str(len_contents)
        if len_contents>1:
            index = '*'

        message = _(associate_messages[index], mapping={'lenassociated':len_contents})
        self.message = message
        result = {}
        values = {
                'relatedcontents': relatedcontents,
                'current_user': user,
                'message': message
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        item['messages'] = all_messages
        item['isactive'] = isactive
        result.update(all_resources)
        result  = merge_dicts(self.requirements_copy, result)
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
        formwidget = deform.widget.FormWidget(css_class='controled-form', 
                                              activable=True,
                                              button_css_class="pull-right",
                                              picto_css_class="glyphicon glyphicon-link",
                                              button_title="Associate")
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='associate',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class AssociateView(MultipleView):
    title = _('Associate the idea')
    name = 'associate'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (RelatedContentsView, AssociateFormView)
    description=_("Associate the idea to an other content")

    def get_message(self):
        message = (associate_messages['0']).format()
        if self.children:
            message = getattr(self.children[0], 'message', message)

        return message


DEFAULTMAPPING_ACTIONS_VIEWS.update({Associate:AssociateView})
