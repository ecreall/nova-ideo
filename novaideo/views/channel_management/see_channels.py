# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
from pyramid.view import view_config
from pyramid import renderers

from dace.objectofcollaboration.principal.util import get_current
from dace.util import getSite
from dace.objectofcollaboration.entity import Entity
from pontus.view import BasicView

from novaideo.content.person import Person
from novaideo.utilities.util import update_all_ajax_action
from novaideo.views.core import asyn_component_config


@asyn_component_config(id='novaideo_see_channels')
@view_config(
    name='seechannels',
    context=Entity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeChannels(BasicView):
    title = ''
    name = 'seechannels'
    template = 'novaideo:views/channel_management/templates/channels.pt'
    viewid = 'seechannels'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def _get_channels_bodies(self, root, user, channels, action_id):
        result_body = []
        for channel in channels:
            subject = channel.get_subject(user)
            actions_call, action_resources = update_all_ajax_action(
                subject, self.request, action_id)
            if actions_call:
                object_values = {
                    'object': channel,
                    'current_user': user,
                    'action_call': actions_call[0]}
                body = renderers.render(
                    channel.templates.get('default'),
                    object_values,
                    self.request)
                result_body.append(body)

        return result_body

    def update(self):
        user = get_current(self.request)
        result = {}
        users_result_body = []
        others_result_body = []
        general_result_body = []
        if self.request.user:
            root = getSite()
            general_channel = root.channel
            channels = getattr(user, 'following_channels', [])
            user_channel = [c for c in channels
                            if isinstance(c.__parent__, Person)]
            generals = [general_channel]
            others = [c for c in channels if c not in user_channel]
            users_result_body = self._get_channels_bodies(
                root, user, user_channel, 'discuss')
            others_result_body = self._get_channels_bodies(
                root, user, others, 'comment')
            general_result_body = self._get_channels_bodies(
                root, user, generals, 'general_discuss')
            general_result_body.extend(others_result_body)

        values = {
            'users_channels': users_result_body,
            'others_channels': general_result_body,
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result
