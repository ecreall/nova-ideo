# -*- coding: utf8 -*-
from pyramid_layout.layout import layout_config


@layout_config(template='views/templates/master.pt')
class GlobalLayout(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
