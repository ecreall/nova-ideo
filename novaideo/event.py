# Copyright (c) 2015 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from zope.interface import implementer
from zope.interface.interfaces import IObjectEvent
from zope.interface import Attribute


class IObjectPublished(IObjectEvent):
    """ An event type sent when an object is published """
    object = Attribute('The object being published')


@implementer(IObjectPublished)
class ObjectPublished(object): # pragma: no cover
    """ An event sent when an object has been published."""
    def __init__(self, object):
        self.object = object


class ICorrelableRemoved(IObjectEvent):
    """ An event type sent when an object is removed """
    object = Attribute('The object being removed')


@implementer(ICorrelableRemoved)
class CorrelableRemoved(object): # pragma: no cover
    """ An event sent when an object has been removed."""
    def __init__(self, object):
        self.object = object


class IObjectModified(IObjectEvent):
    """ An event type sent when an object is modified """
    object = Attribute('The object being modified')


@implementer(IObjectModified)
class ObjectModified(object): # pragma: no cover
    """ An event sent when an object has been modified."""
    def __init__(self, object, args):
        self.object = object
        self.args = args
