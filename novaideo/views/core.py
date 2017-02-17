# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi, Sophie Jazwiecki

from pontus.view import BasicView

from novaideo import _


class ActionAnonymousView(BasicView):
    title = _('Alert for comment')
    template = 'novaideo:views/templates/alert_action_anonymous.pt'

    def update(self):
        self.execute(None)
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ComponentView(BasicView):
    title = ''
    template = 'novaideo:views/templates/component_view.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    component_id = ''

    def update(self):
        self.execute(None)
        result = {}
        body = self.content(
            args={'id': self.component_id},
            template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result
