from pyramid.events import subscriber

from substanced.event import RootAdded
from substanced.util import find_service


@subscriber(RootAdded)
def mysubscriber(event):
    root = event.object
    principals = find_service(root, 'principals')
    users = principals['users']
