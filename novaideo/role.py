# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from dace.objectofcollaboration.principal.util import (
  has_role, get_current)
from dace.objectofcollaboration.principal.role import (
    Collaborator, Role, Administrator, role)

from novaideo import _


@role(name='SiteAdmin',
      superiors=[Administrator])
class SiteAdmin(Role):
    pass


@role(name='Member',
      superiors=[Administrator, SiteAdmin],
      lowers=[Collaborator])
class Member(Role):
    pass


@role(name='PortalManager',
      superiors=[Administrator, SiteAdmin],
      lowers=[Collaborator, Member])
class PortalManager(Role):
    pass


@role(name='Observer',
      superiors=[Administrator, SiteAdmin],
      lowers=[Collaborator],
      islocal=True)
class Observer(Role):
    pass


@role(name='Moderator',
      superiors=[Administrator, SiteAdmin],
      lowers=[Collaborator, Member, PortalManager])
class Moderator(Role):
    pass


@role(name='Examiner',
      superiors=[Administrator, SiteAdmin],
      lowers=[Collaborator, Member, Moderator])
class Examiner(Role):
    pass


@role(name='OrganizationResponsible',
      superiors=[Administrator, SiteAdmin],
      lowers=[Collaborator],
      islocal=True)
class OrganizationResponsible(Role):
    pass


@role(name='Participant',
      superiors=[Administrator, SiteAdmin],
      lowers=[Collaborator, Observer],
      islocal=True)
class Participant(Role):
    pass


@role(name='Elector',
      islocal=True)
class Elector(Role):
    pass


@role(name='ChallengeParticipant',
      islocal=True)
class ChallengeParticipant(Role):
    pass


@role(name='Certifier',
      superiors=[Administrator, SiteAdmin],
      lowers=[Collaborator])
class Certifier(Role):
    pass


@role(name='Bot', superiors=[Administrator])
class Bot(Role):
    pass


def get_authorized_roles(user=None):
    if not user:
        user = get_current()

    roles = APPLICATION_ROLES.copy()
    if not has_role(user=user, role=('SiteAdmin', )) and \
       'SiteAdmin' in roles:
        roles.pop('SiteAdmin')

    if not has_role(user=user, role=('Admin', )) and \
       'Admin' in roles:
        roles.pop('Admin')

    return roles


DEFAULT_ROLES = ['Member']


APPLICATION_ROLES = {
    'Member': _('Member'),
    'Admin': _('Administrator'),
    'SiteAdmin': _('Site administrator'),
    'Moderator': _('Moderator'),
    'Examiner': _('Examiner'),
}
