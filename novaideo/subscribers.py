from pyramid.events import subscriber

from substanced.event import RootAdded
from substanced.util import find_service

from dace.objectofcollaboration.principal.util import grant_roles


@subscriber(RootAdded)
def mysubscriber(event):
    root = event.object
    catalogs = find_service(root, 'catalogs')
    catalogs.add_catalog('novaideo')
    principals = find_service(root, 'principals')
    users = principals['users']
