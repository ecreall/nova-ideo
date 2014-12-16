# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedUniqueProperty
from pontus.core import VisualisableElement

from .interface import IToken


@content(
    'token',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IToken)
class Token(VisualisableElement, Entity):
    """Token class""" 

    name = renamer()
    owner = SharedUniqueProperty('owner')
    proposal = SharedUniqueProperty('proposal')