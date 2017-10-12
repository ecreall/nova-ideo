
from zope.interface import implementer

from substanced.util import renamer

from dace.objectofcollaboration.principal import Group
from dace.descriptors import (
    SharedUniqueProperty,
    SharedMultipleProperty)

from novaideo.content.interface import IMask
from novaideo.core import AnonymisationKinds


@implementer(IMask)
class Mask(Group):

    name = renamer()
    member = SharedUniqueProperty('member', 'mask')
    ideas = SharedMultipleProperty('ideas', 'author')
    working_groups = SharedMultipleProperty('working_groups', 'members')
    questions = SharedMultipleProperty('questions', 'author')
    challenges = SharedMultipleProperty('challenges', 'author')
    templates = {'card': 'novaideo:views/templates/anonymous_card.pt',}
    default_picture = 'novaideo:static/images/anonymous100.png'
    is_anonymous = True

    def __init__(self, **kwargs):
        super(Mask, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def title(self):
        default_title = 'Anonymous'
        root = getattr(self, '__parent__', None)
        anonymisation_kind = getattr(
            root, 'anonymisation_kind',
            AnonymisationKinds.anonymity)
        if anonymisation_kind == AnonymisationKinds.anonymity:
            return default_title

        name = self.name
        return name if name else default_title


    @property
    def first_name(self):
        return 'Anonymous'

    @property
    def last_name(self):
        return 'Anonymous'

    @property
    def email(self):
        return getattr(self.member, 'email', '')

    @property
    def user_locale(self):
        return getattr(self.member, 'user_locale', '')

    @property
    def proposals(self):
        return [wg.proposal for wg in self.working_groups]

    @property
    def participations(self):
        result = [p for p in list(self.proposals)
                  if any(s in p.state for s
                         in ['amendable',
                             'open to a working group',
                             'votes for publishing',
                             'votes for amendments'])]
        return result

    @property
    def contents(self):
        result = [i for i in list(self.ideas) if i is i.current_version]
        result.extend(self.proposals)
        result.extend(self.questions)
        result.extend(self.challenges)
        return result

    @property
    def active_working_groups(self):
        return [p.working_group for p in self.participations]

    def reindex(self):
        super(Mask, self).reindex()
        if self.member:
            self.member.reindex()
