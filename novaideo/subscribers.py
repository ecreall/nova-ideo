# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import transaction
from pyramid.events import subscriber, ApplicationCreated
from pyramid.threadlocal import get_current_registry, get_current_request
from pyramid.request import Request
from pyramid.threadlocal import manager

from substanced.event import RootAdded
from substanced.util import find_service

from dace.util import getSite

from novaideo.ips.mailer import mailer_send
from novaideo import core
from novaideo.event import ObjectPublished, CorrelableRemoved
from novaideo.views.filter import get_users_by_keywords
from novaideo import _


_CONTENT_TRANSLATION = [_("The proposal"),
                        _("The idea")]


@subscriber(RootAdded)
def mysubscriber(event):
    """Add the novaideo catalog when the root is added."""
    root = event.object
    registry = get_current_registry()
    settings = registry.settings
    novaideo_title = settings.get('novaideo.title')
    root.title = novaideo_title
    root.init_files()
    catalogs = find_service(root, 'catalogs')
    catalogs.add_catalog('novaideo')


@subscriber(ObjectPublished)
def mysubscriber_object_published(event):
    content = event.object
    keywords = content.keywords
    request = get_current_request()
    users = get_users_by_keywords(keywords)
    url = request.resource_url(content, "@@index")
    root = request.root
    mail_template = root.get_mail_template('alert_new_content')
    subject = mail_template['subject'].format(subject_title=content.title)
    localizer = request.localizer
    for member in [m for m in users if getattr(m, 'email', '')]:
        message = mail_template['template'].format(
            recipient_title=localizer.translate(_(getattr(member,
                                                        'user_title', ''))),
            recipient_first_name=getattr(member, 'first_name', member.name),
            recipient_last_name=getattr(member, 'last_name', ''),
            subject_title=content.title,
            subject_url=url,
            subject_type=localizer.translate(
                _("The " + content.__class__.__name__.lower())),
            novaideo_title=root.title
             )
        mailer_send(
            subject=subject,
            recipients=[member.email],
            sender=root.get_site_sender(),
            body=message)


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
    [source_correlations.extend(getattr(version, 'source_correlations', []))
     for version in all_versions]
    #destroy all versions
    if hasattr(removed_object, 'destroy'):
        removed_object.destroy()

    #update correlations
    for correlation in source_correlations:
        for target in list(correlation.targets):
            correlation.delfromproperty('targets', target)

        root.delfromproperty('correlations', correlation)


@subscriber(ApplicationCreated)
def init_application(event):
    app = event.object
    registry = app.registry
    request = Request.blank('/application_created') # path is meaningless
    request.registry = registry
    manager.push({'registry': registry, 'request': request})
    root = app.root_factory(request)
    request.root = root
    root.init_files()
    # other init functions
    init_contents(registry)

    transaction.commit()
    manager.pop()


def init_contents(registry):
    """Init searchable content"""
    core.SEARCHABLE_CONTENTS = {
        type_id: c
        for type_id, c in registry.content.content_types.items()
        if core.SearchableEntity in c.mro()
    }
