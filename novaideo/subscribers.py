
from pyramid.events import subscriber

from substanced.event import RootAdded
from substanced.util import find_service


@subscriber(RootAdded)
def mysubscriber(event):
    """Add the novaideo catalog when the root is added."""

    root = event.object
    catalogs = find_service(root, 'catalogs')
    catalogs.add_catalog('novaideo')
    #principals = find_service(root, 'principals')
    #users = principals['users'] 
