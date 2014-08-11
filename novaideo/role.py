from dace.objectofcollaboration.principal.role import (
    Collaborator, Role, Administrator, role)


@role(name='Member',
      superiors=[Administrator],
      lowers=[Collaborator])
class Member(Role):
    pass


@role(name='Observer',
      superiors=[Administrator],
      lowers=[Collaborator],
      islocal=True)
class Observer(Role):
    pass


@role(name='Moderator',
      superiors=[Administrator],
      lowers=[Collaborator])
class Moderator(Role):
    pass


@role(name='Examiner',
      superiors=[Administrator],
      lowers=[Collaborator])
class Examiner(Role):
    pass


@role(name='OrganizationResponsible',
      superiors=[Administrator],
      lowers=[Collaborator],
      islocal=True)
class OrganizationResponsible(Role):
    pass


@role(name='Participant',
      superiors=[Administrator],
      lowers=[Collaborator, Observer],
      islocal=True)
class Participant(Role):
    pass


@role(name='Certifier',
     superiors=[Administrator],
     lowers=[Collaborator])
class Certifier(Role):
    pass
