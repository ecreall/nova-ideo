# -*- coding: utf-8 -*-
from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import CompositeMultipleProperty
from pontus.core import VisualisableElement
from pontus.widget import SequenceWidget

from .interface import ICommentabl
from novaideo import _



@content(
    'commentabl',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICommentabl)
class Commentabl(VisualisableElement, Entity):
    name = renamer()
    attached_files = CompositeMultipleProperty('attached_files')
    comments = CompositeMultipleProperty('comments')

    def __init__(self, **kwargs):
        super(Commentabl, self).__init__(**kwargs)

