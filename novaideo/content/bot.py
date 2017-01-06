# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer

from dace.descriptors import CompositeUniqueProperty
from dace.objectofcollaboration.principal import Machine

from .interface import (
    IBot)


@content(
    'bot',
    icon='icon glyphicon glyphicon-user',
    )
@implementer(IBot)
class Bot(Machine):
    """Bot class"""

    icon = 'icon glyphicon glyphicon-user'
    name = renamer()
    picture = CompositeUniqueProperty('picture')

    def __init__(self, **kwargs):
        super(Bot, self).__init__(**kwargs)
        self.set_data(kwargs)

    def get_picture_url(self, kind, default):
        if self.picture:
            img = getattr(self.picture, kind, None)
            if img:
                return img.url

        return default
