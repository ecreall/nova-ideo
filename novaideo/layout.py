# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import os
import pytz
import datetime
from pyramid_layout.layout import layout_config

from novaideo.utilities.util import (
    to_localized_time, get_emoji_form, EMOJI_TEMPLATE,
    render_files, render_files_slider)
from novaideo.utilities.analytics_utility import get_colors
from novaideo.emojis import DEFAULT_EMOJIS
from novaideo.lib import config


@layout_config(template='views/templates/master.pt')
class GlobalLayout(object):

    emoji_template = 'novaideo:views/templates/emoji_selector.pt'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def to_localized_time(
        self, date, date_from=None,
        date_only=False, format_id='digital',
        ignore_month=False, ignore_year=False,
        add_day_name=False):
        if not date:
            return ''

        if isinstance(date, datetime.datetime):
            date = date.replace(tzinfo=pytz.UTC)
            date = date.astimezone(self.request.get_time_zone)

        return to_localized_time(
            date, request=self.request, date_from=date_from,
            date_only=date_only, format_id=format_id,
            ignore_month=ignore_month, ignore_year=ignore_year,
            add_day_name=add_day_name, translate=True)

    def get_emoji_form(
        self, template=EMOJI_TEMPLATE, emoji_class='',
        groups=DEFAULT_EMOJIS, is_grouped=True):
        return get_emoji_form(
            self.request,
            template=template,
            emoji_class=emoji_class,
            groups=groups,
            is_grouped=is_grouped)

    def render_files(self, files):
        return render_files(files, self.request)

    def render_files_slider(self, slider_id, files_data, deferred=False):
        return render_files_slider(
            slider_id, files_data, self.request, deferred=deferred)

    def get_colors(self, nb):
        return get_colors(count=nb)

    def get_root(self):
        novaideo_config = config.get_config()
        use_webpack_server = novaideo_config.get('use_webpack_server', False)
        root_url = 'static-react'
        node_env = os.getenv('NODE_MODE', 'production')
        if use_webpack_server:
            root_url = 'http://{}:{}'.format(
                novaideo_config.get('webpack_host', 'localhost'),
                novaideo_config.get('webpack_port', 8081))

        return {'root_url': root_url, 'node_env': node_env}
