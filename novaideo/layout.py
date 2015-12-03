# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid_layout.layout import layout_config

from novaideo.utilities.util import to_localized_time


@layout_config(template='views/templates/master.pt')
class GlobalLayout(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def to_localized_time(
        self, date, date_from=None,
        date_only=False, format_id='digital',
        ignore_month=False, ignore_year=False,
        add_day_name=False):
        return to_localized_time(
            date, request=self.request, date_from=date_from,
            date_only=date_only, format_id=format_id,
            ignore_month=ignore_month, ignore_year=ignore_year,
            add_day_name=add_day_name, translate=True)
