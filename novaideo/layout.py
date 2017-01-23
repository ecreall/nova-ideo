# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
import pytz
import datetime
from pyramid_layout.layout import layout_config

from novaideo.utilities.util import (
    to_localized_time, get_emoji_form, EMOJI_TEMPLATE,
    render_files)
from novaideo.utilities.analytics_utility import get_colors
from novaideo.emojis import DEFAULT_EMOJIS


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

    def get_colors(self, nb):
        return get_colors(count=nb)
