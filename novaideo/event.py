
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