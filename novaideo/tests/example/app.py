# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Sophie Jazwiecki

from substanced.util import find_service

from dace.objectofcollaboration.object import Object
from dace.util import name_chooser
from dace.objectofcollaboration.principal.util import grant_roles


class SubjectType(Object):
    pass


class User(Object):
    pass


def add_user(data, request, roles=('Member',)):
    from novaideo.content.person import Person
    root = request.root
    person = Person(**data)
    principals = find_service(root, 'principals')
    name = person.first_name + ' ' + person.last_name
    users = principals['users']
    name = name_chooser(users, name=name)
    users[name] = person
    grant_roles(person, roles=roles)
    grant_roles(person, (('Owner', person),))
    person.state.append('active')
    person.init_annotations()
    person.reindex()
    return person
