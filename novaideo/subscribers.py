
from pyramid.events import subscriber

from substanced.event import RootAdded
from substanced.util import find_service

from novaideo.core import FileEntity


@subscriber(RootAdded)
def mysubscriber(event):
    """Add the novaideo catalog when the root is added."""

    root = event.object
    catalogs = find_service(root, 'catalogs')
    catalogs.add_catalog('novaideo')
    ml_file = FileEntity()
    ml_file.__name__ = 'ml_file'
    root.addtoproperty('files', ml_file)
    root.ml_file = ml_file
    #principals = find_service(root, 'principals')
    #users = principals['users'] 
