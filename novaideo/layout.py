# -*- coding: utf8 -*-
from pyramid_layout.layout import layout_config


@layout_config(template='views/templates/master.pt')
class GlobalLayout(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def to_localized_time(self, date, date_only=False):
        if date_only:
            return date.strftime('%d/%m/%Y')
        else:
            return date.strftime('%d/%m/%Y %H:%M')
