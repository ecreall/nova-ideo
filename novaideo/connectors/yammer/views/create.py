# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.connectors.yammer.content.behaviors import CreateConnector
from novaideo.connectors.yammer import YammerConnectorSchema, YammerConnector
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='createyammerconnector',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateYammerConnectorView(FormView):

    title = _('Add a Yammer connector')
    schema = select(YammerConnectorSchema(factory=YammerConnector, editable=True),
                    ['auth_conf',
                     'notif_conf'])
    behaviors = [CreateConnector, Cancel]
    formid = 'formcreateyammerconnector'
    name = 'createyammerconnector'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CreateConnector: CreateYammerConnectorView})
