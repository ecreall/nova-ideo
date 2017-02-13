# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from dace.interfaces import (
    Attribute, IUser, IEntity as IEntityO, IApplication,
    IMachine)

from pontus.interfaces import IVisualisableElement, IImage as SourceIImage

from novaideo.utilities.data_manager import (
    interface_config,
    IMAGETYPE,
    FILETYPE,
    file_deserializer,
    interface,
    sub_object_serialize)


def get_subinterfaces(interface):
    result = list(getattr(interface, '__sub_interfaces__', []))
    for sub_interface in list(result):
        if getattr(sub_interface, 'is_abstract', False):
            result.extend(get_subinterfaces(sub_interface))

    result.append(interface)
    return list(set(result))


@interface(True)
class IEntity(IEntityO):
    pass


@interface(True)
class IIdeaSource(IEntityO):
    pass


@interface()
@interface_config(type_id='creation_culturelle_image',
                  deserializer=file_deserializer,
                  serializer=sub_object_serialize)
class IImage(SourceIImage):
    pass


@interface()
class INewsletter(IVisualisableElement, IEntity):
    pass


@interface(True)
class INode(IEntity):
    pass


@interface(True)
class IEmojiable(IEntity):
    pass


@interface()
class ICorrection(IEntity):
    pass


@interface(True)
class IPresentableEntity(IEntity):
    pass


@interface()
class IVote(IEntity):
    pass


@interface()
class IBallotType(IEntity):
    pass


@interface()
class IReport(IEntity):
    pass


@interface()
class IBallot(IEntity):
    pass


@interface()
class IBallotBox(IEntity):
    pass


@interface(True)
class ICorrelableEntity(IEntity):
    pass


@interface(True)
class ISearchableEntity(IEntity):

    name = Attribute('name')

    title = Attribute('title')

    description = Attribute('description')

    keywords = Attribute('keywords')

    author = Attribute('author', type='person')


@interface(True)
class IVersionableEntity(IEntity):
    pass


@interface(True)
class IDuplicableEntity(IEntity):
    pass


@interface(True)
class ICommentable(IEntity):
    pass


@interface(True)
class IDebatable(IEntity):
    pass


@interface(True)
class ISignalableEntity(IEntity):
    pass


@interface(True)
class ISustainable(IEntity):
    pass


@interface(True)
class ITokenable(IEntity):
    pass


@interface()
class ISReport(IEntity):
    pass


@interface()
@interface_config(type_id='idea')
class IChallenge(ISearchableEntity,
                 ICorrelableEntity,
                 IPresentableEntity,
                 INode,
                 ISignalableEntity,
                 IDebatable):
    pass


@interface()
class IComment(ICommentable, IIdeaSource, ISignalableEntity):
    pass


@interface()
class IChannel(ICommentable):
    pass


@interface()
class IPrivateChannel(IChannel):
    pass


@interface()
@interface_config(type_id='amendment')
class IAmendment(ICorrelableEntity,
                 IPresentableEntity,
                 IDuplicableEntity,
                 ISearchableEntity,
                 IDebatable):

    text = Attribute('text')


@interface()
@interface_config(type_id='idea')
class Iidea(IDuplicableEntity,
            IVersionableEntity,
            ISearchableEntity,
            ICorrelableEntity,
            IPresentableEntity,
            INode,
            ISignalableEntity,
            IDebatable,
            ITokenable):

    text = Attribute('text')

    attached_files = Attribute('attached_files', type=FILETYPE, multiplicity='*')


@interface()
@interface_config(type_id='question')
class IQuestion(IDuplicableEntity,
                IVersionableEntity,
                ISearchableEntity,
                ICorrelableEntity,
                IPresentableEntity,
                INode,
                ISignalableEntity,
                ISustainable,
                IDebatable):
    question = Attribute('question')

    text = Attribute('text')

    attached_files = Attribute('attached_files', type=FILETYPE, multiplicity='*')


@interface()
@interface_config(type_id='answer')
class IAnswer(ICorrelableEntity,
              IPresentableEntity,
              INode,
              IIdeaSource,
              ISignalableEntity,
              ISustainable,
              IDebatable):
    comment = Attribute('comment')

    attached_files = Attribute('attached_files', type=FILETYPE, multiplicity='*')


@interface()
class IFile(ISearchableEntity):
    pass


@interface()
class ICorrelation(IEntity, IDebatable):
    pass


@interface()
class IInvitation(IEntity):
    pass


@interface()
class IKeyword(IEntity):
    pass


@interface()
class ICandidacy(IEntity):
    pass


@interface()
class IToken(IEntity):
    pass


@interface(True)
class IBaseUser(IEntity):

    first_name = Attribute('first_name')

    last_name = Attribute('last_name')

    user_title = Attribute('user_title')

    organization = Attribute('organization', type='organization')


@interface()
@interface_config(type_id='person')
class IPerson(IVisualisableElement,
              ISearchableEntity,
              ICorrelableEntity,
              IBaseUser,
              IUser,
              IDebatable):

    picture = Attribute('picture', type=IMAGETYPE)


@interface()
@interface_config(type_id='bot')
class IBot(IMachine):

    picture = Attribute('picture', type=IMAGETYPE)


@interface()
@interface_config(type_id='preregistration')
class IPreregistration(IBaseUser):
    pass


@interface()
@interface_config(type_id='proposal')
class IProposal(ISearchableEntity,
                ICorrelableEntity,
                IDuplicableEntity,
                IPresentableEntity,
                INode,
                ISignalableEntity,
                IDebatable,
                ITokenable):

    text = Attribute('text')

    attached_files = Attribute('attached_files', type=FILETYPE, multiplicity='*')

    workspace = Attribute('workspace', type='workspace')

    working_group = Attribute('working_group', type='workinggroup')

    authors = Attribute('authors', type='person', multiplicity='*')

    related_ideas = Attribute('related_ideas', type='idea', multiplicity='*')


@interface()
@interface_config(type_id='workinggroup')
class IWorkingGroup(IEntity):
    pass


@interface()
@interface_config(type_id='workspace')
class IWorkspace(IVisualisableElement,
                 IEntity):

    files = Attribute('files', type=FILETYPE, multiplicity='*')


@interface()
@interface_config(type_id='organization')
class IOrganization(IEntity):
    pass


@interface()
class INovaIdeoApplication(IEntity, IApplication, IIdeaSource, IDebatable):
    pass


@interface()
@interface_config(type_id='alert')
class IAlert(IVisualisableElement,
             IEntity):
    pass


@interface(True)
class IAdvertising(IVisualisableElement, ISearchableEntity):

    dates = Attribute('dates')


@interface()
@interface_config(type_id='web_advertising')
class IWebAdvertising(IAdvertising):

    picture = Attribute('picture', type=FILETYPE)

    html_content = Attribute('html_content')

    advertisting_url = Attribute('advertisting_url')


@interface()
@interface_config(type_id='smartfolder')
class ISmartFolder(IVisualisableElement, IEntity):

    view_type = Attribute('view_type')

    children = Attribute('children', type='smartfolder', multiplicity='*')

    style = Attribute('style')
