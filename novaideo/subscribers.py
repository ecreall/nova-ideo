# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.events import subscriber
from pyramid.threadlocal import get_current_registry

from substanced.event import RootAdded
from substanced.util import find_service

from dace.util import getSite

from novaideo.core import FileEntity
from novaideo.utilities.util import send_alert_new_content
from novaideo.event import ObjectPublished, CorrelableRemoved


@subscriber(RootAdded)
def mysubscriber(event):
    """Add the novaideo catalog when the root is added."""
    root = event.object
    registry = get_current_registry()
    settings = registry.settings
    novaideo_title = settings.get('novaideo.title')
    root.title = novaideo_title
    catalogs = find_service(root, 'catalogs')
    catalogs.add_catalog('novaideo')
    ml_file = FileEntity(title="Legal notices")
    ml_file.__name__ = 'ml_file'
    root.addtoproperty('files', ml_file)
    root.ml_file = ml_file
    terms_of_use = FileEntity(title="Terms of use")
    terms_of_use.__name__ = 'terms_of_use'
    root.addtoproperty('files', terms_of_use)
    root.terms_of_use = terms_of_use
    #password = settings.get('ineus.initial_password')
    #admin = Person(password=password, email=login)
    #admin.__name__ = 'ineus_admin'
    #principals = find_service(root, 'principals')
    #principals['users'][admin.__name__] = admin
    #grant_roles(user=admin, roles=('Admin',))


@subscriber(ObjectPublished)
def mysubscriber_object_published(event):
    published_object = event.object
    send_alert_new_content(published_object)


@subscriber(CorrelableRemoved)
def mysubscriber_correlable_removed(event):
    root = getSite()
    removed_object = event.object
    #get all versions. Versions will be removed
    all_versions = getattr(removed_object, 'history', [])
    if removed_object in all_versions:
        all_versions.remove(removed_object)

    #recuperate all correlations
    source_correlations = removed_object.source_correlations
    [source_correlations.extend(getattr(version,'source_correlations', [])) \
     for version in all_versions]
    #destroy all versions
    if hasattr(removed_object, 'destroy'):
        removed_object.destroy()
    
    #update correlations
    for correlation in source_correlations:
        for target in list(correlation.targets):
            correlation.delfromproperty('targets', target)

        root.delfromproperty('correlations', correlation)

