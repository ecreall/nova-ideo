# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
from deform.widget import default_resource_registry


class YammerNotificationWidget(deform.widget.TextInputWidget):
    template = 'novaideo:connectors/yammer/views/templates/yammer_notification.pt'
    requirements = ( ('yammer_notification', None), )


default_resource_registry.set_js_resources('yammer_notification', None,
               'novaideo:static/connectors/yammer/yammer_notification.js' )
