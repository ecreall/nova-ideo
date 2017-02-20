# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi, Sophie Jazwiecki
import venusian

from pontus.view import BasicView

from novaideo import _
from novaideo.core import ON_LOAD_VIEWS


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
    css_class = 'simple-bloc async-component-container'
    container_css_class = 'home async-component'

    def __init__(self,
                 context,
                 request,
                 **kwargs):
        super(ComponentView, self).__init__(context, request, **kwargs)
        self.component_id = kwargs.get('component_id', '')

    def update(self):
        result = {}
        body = self.content(
            args={'id': self.component_id},
            template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class asyn_component_config(object):
    """ A function, class or method decorator which allows a
    developer to create async component (view or sub-view).
    """
    def __init__(self, id, loading_component=ComponentView):
        self.component_id = id
        self.loading_component = loading_component

    def __call__(self, wrapped):
        def callback(scanner, name, ob):
            ob.component_id = self.component_id
            ob.loading_component = self.loading_component
            old_call = ob.update

            def update(self):
                if not self.params('load_view'):
                    component = self.loading_component(
                        self.context, self.request,
                        component_id=self.component_id)
                    component.wrapper_template = ob.wrapper_template
                    component.css_class = ob.css_class + ' async-component-container'
                    component.container_css_class = ob.container_css_class + \
                        ' async-component'
                    return component.update()

                return old_call(self)

            ob.update = update
            ON_LOAD_VIEWS[self.component_id] = ob

        venusian.attach(wrapped, callback, category='site_widget')
        return wrapped
