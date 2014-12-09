# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.events import subscriber

from substanced.event import RootAdded
from substanced.util import find_service

from novaideo.core import FileEntity
from novaideo.utilities.util import send_alert_new_content
from novaideo.event import ObjectPublished


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


@subscriber(ObjectPublished)
def mysubscriber_object_published(event):
    published_object = event.object
    send_alert_new_content(published_object)