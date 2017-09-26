# Copyright (c) 2015 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

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
        item['isactive'] = getattr(self, 'isactive', False)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class asyn_component_config(object):
    """ A function, class or method decorator which allows a
    developer to create async component (view or sub-view).
    """
    def __init__(self, id, loading_component=ComponentView, on_demand=False, delegate=None):
        self.component_id = id
        self.loading_component = loading_component
        self.on_demand = on_demand
        self.delegate = delegate

    def __call__(self, wrapped):
        def callback(scanner, name, ob):
            ob.component_id = self.component_id
            ob.loading_component = self.loading_component
            ob.on_demand = self.on_demand
            ob.delegate = self.delegate
            old_call = ob.update

            def update(self):
                if not self.params('load_view') or (self.on_demand and self.params('on_demand') != 'load'):
                    component = self.loading_component(
                        self.context, self.request,
                        component_id=self.component_id)
                    component.wrapper_template = ob.wrapper_template
                    component.title = ob.title
                    component.viewid = ob.viewid
                    component.view_icon = getattr(ob, 'view_icon', '')
                    component.counter_id = getattr(ob, 'counter_id', '')
                    component.css_class = ob.css_class + ' async-component-container'
                    component.container_css_class = ob.container_css_class + \
                        ' async-component'
                    component.isactive = getattr(ob, 'isactive', False)
                    return component.update()

                return old_call(self)

            ob.update = update
            ON_LOAD_VIEWS[self.component_id] = ob

        venusian.attach(wrapped, callback, category='site_widget')
        return wrapped
