# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from zope.interface import Interface

from dace.interfaces import Attribute, IUser, IEntity as IEntityO, IApplication

from pontus.interfaces import IVisualisableElement

from novaideo.utilities.data_manager import (
    interface_config,
    OBJECTTYPE,
    IMAGETYPE,
    FILETYPE,
    file_deserializer)


class IEntity(IEntityO):
    pass


class ICorrection(Interface):
    pass


class IPresentableEntity(Interface):
    pass


class IVote(Interface):
    pass


class IBallotType(Interface):
    pass


class IReport(Interface):
    pass


class IBallot(Interface):
    pass


class IBallotBox(Interface):
    pass


class ICorrelableEntity(Interface):
    pass


class ISearchableEntity(Interface):
    pass


class IVersionableEntity(Interface):
    pass


class IDuplicableEntity(Interface):
    pass


class ISearchableEntity(IEntity):
    pass


class ICommentable(Interface):
    pass


class IComment(ICommentable):
    pass


class IAmendment(ICommentable, 
                 ICorrelableEntity,
                 IPresentableEntity,
                 IDuplicableEntity,
                 ISearchableEntity):
    pass


class Iidea(ICommentable,
            IDuplicableEntity,
            IVersionableEntity,
            ISearchableEntity,
            ICorrelableEntity,
            IPresentableEntity):
    pass


class IFile(ISearchableEntity):
    pass

class ICorrelation(ICommentable):
    pass


class IInvitation(Interface):
    pass


class IKeyword(Interface):
    pass


class ICandidacy(Interface):
    pass


class IToken(Interface):
    pass


class IPerson(ISearchableEntity,
              ICorrelableEntity):
    pass


class IBaseUser(IEntity):

    first_name = Attribute('first_name')

    last_name = Attribute('last_name')

    user_title = Attribute('user_title')


@interface_config(type_id='person')
class IPerson(IVisualisableElement,
              ISearchableEntity,
              ICorrelableEntity,
              IBaseUser,
              IUser):

    picture = Attribute('picture', type=IMAGETYPE)


class IPreregistration(IBaseUser):
    pass


class IProposal(ICommentable,
                ISearchableEntity,
                ICorrelableEntity,
                IDuplicableEntity,
                IPresentableEntity):
    pass


class IWorkingGroup(Interface):
    pass


class IOrganization(Interface):
    pass


class INovaIdeoApplication(IApplication):
    pass
