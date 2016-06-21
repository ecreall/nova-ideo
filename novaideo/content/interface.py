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


class INode(IEntity):
    pass


class ICorrection(IEntity):
    pass


class IPresentableEntity(IEntity):
    pass


class IVote(IEntity):
    pass


class IBallotType(IEntity):
    pass


class IReport(IEntity):
    pass


class IBallot(IEntity):
    pass


class IBallotBox(IEntity):
    pass


class ICorrelableEntity(IEntity):
    pass


class ISearchableEntity(IEntity):
    pass


class IVersionableEntity(IEntity):
    pass


class IDuplicableEntity(IEntity):
    pass


class ICommentable(IEntity):
    pass


class IComment(ICommentable):
    pass


class IChannel(ICommentable):
    pass


class IPrivateChannel(IChannel):
    pass


class IAmendment(ICorrelableEntity,
                 IPresentableEntity,
                 IDuplicableEntity,
                 ISearchableEntity):
    pass


class Iidea(IDuplicableEntity,
            IVersionableEntity,
            ISearchableEntity,
            ICorrelableEntity,
            IPresentableEntity,
            INode):
    pass


class IFile(ISearchableEntity):
    pass


class ICorrelation(IEntity):
    pass


class IInvitation(IEntity):
    pass


class IKeyword(IEntity):
    pass


class ICandidacy(IEntity):
    pass


class IToken(IEntity):
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


class IProposal(ISearchableEntity,
                ICorrelableEntity,
                IDuplicableEntity,
                IPresentableEntity,
                INode):
    pass


class IWorkingGroup(IEntity):
    pass


class IWorkspace(IVisualisableElement,
                 IEntity):
    pass


class IOrganization(IEntity):
    pass


class INovaIdeoApplication(IEntity, IApplication):
    pass


class IAlert(IVisualisableElement,
             IEntity):
    pass


class IAdvertising(IVisualisableElement, ISearchableEntity):

    dates = Attribute('dates')


@interface_config(type_id='web_advertising')
class IWebAdvertising(IAdvertising):

    picture = Attribute('picture', type=FILETYPE)

    html_content = Attribute('html_content')

    advertisting_url = Attribute('advertisting_url')
