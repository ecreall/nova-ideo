# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import transaction
import datetime
import pytz
import transaction
from persistent.list import PersistentList
from pyramid.security import remember

from substanced.util import find_service, get_oid
from substanced.event import LoggedIn

from dace.objectofcollaboration.principal.util import (
    grant_roles,
    has_role)
from dace.util import name_chooser, find_catalog, getSite
from dace.processinstance.core import PROCESS_HISTORY_KEY

from novaideo import my_locale_negotiator
from novaideo.content.person import Person
from novaideo.content.interface import IPerson


def create_user(request, appstruct):
    if appstruct and 'user_data' in appstruct:
        source_data = appstruct.get('source_data', {})
        data = appstruct.get('user_data', {})
        root = getSite()
        locale = my_locale_negotiator(request)
        data['locale'] = locale
        person = Person(**data)
        person.set_source_data(source_data)
        principals = find_service(root, 'principals')
        name = person.first_name + ' ' + person.last_name
        users = principals['users']
        name = name_chooser(users, name=name)
        users[name] = person
        grant_roles(person, roles=('Member',))
        grant_roles(person, (('Owner', person),))
        person.state.append('active')
        person.init_annotations()
        person.annotations.setdefault(
            PROCESS_HISTORY_KEY, PersistentList())
        person.reindex()
        root.addtoproperty('news_letter_members', person)
        newsletters = root.get_newsletters_automatic_registration()
        email = getattr(person, 'email', '')
        if newsletters and email:
            for newsletter in newsletters:
                newsletter.subscribe(
                    person.first_name, person.last_name, email)

        transaction.commit()
        return person

    return None


def get_or_create_user(request, appstruct, set_source_data=True):
    user_id = appstruct.get('user_data', {}).get('email', None)
    if not user_id:
        source_data = appstruct.get('source_data', {})
        user_id = source_data.get('app_name', '') + '_' +\
            source_data.get('id', '')

    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    identifier_index = novaideo_catalog['identifier']
    object_provides_index = dace_catalog['object_provides']
    query = object_provides_index.any([IPerson.__identifier__]) &\
        identifier_index.any([user_id])
    users = list(query.execute().all())
    user = users[0] if users else None
    if user is None:
        user = create_user(request, appstruct)
    elif set_source_data:
        user.set_source_data(appstruct.get('source_data', {}))

    return user


def validate_user(context, request, appstruct):
    user = get_or_create_user(request, appstruct)
    valid = user and (has_role(user=user, role=('SiteAdmin', )) or
                      'active' in getattr(user, 'state', []))
    headers = None
    if valid:
        request.session.pop('novaideo.came_from', None)
        headers = remember(request, get_oid(user))
        request.registry.notify(
            LoggedIn(
                user.email, user,
                context, request))
        user.last_connection = datetime.datetime.now(tz=pytz.UTC)
        if hasattr(user, 'reindex'):
            user.reindex()

    return user, valid, headers
