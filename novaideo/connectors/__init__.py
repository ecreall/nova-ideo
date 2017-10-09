# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.interfaces import IEntity
from pontus.interfaces import IVisualisableElement
from pontus.core import VisualisableElementSchema

from novaideo import _
from novaideo.core import VersionableEntity
from novaideo.utilities.data_manager import interface


@interface()
class IConnector(IVisualisableElement, IEntity):
    pass


class ConnectorSchema(VisualisableElementSchema):
    """Schema for idea"""
    pass


@content(
    'connector',
    icon='icon novaideo-icon icon-idea',
    )
@implementer(IConnector)
class Connector(VersionableEntity, Entity):
    """Connector class"""

    type_title = _('Connector')
    connector_id = 'connector'
    icon = 'icon fa fa-plug'
    name = renamer()

    def __init__(self, **kwargs):
        super(Connector, self).__init__(**kwargs)
        self.set_data(kwargs)

    def get_access_tokens(self, user):
        return {}

    def extract_data(self, sources):
        return {}, {}
