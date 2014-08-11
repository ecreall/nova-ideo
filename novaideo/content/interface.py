from zope.interface import Interface


class ICorrelableEntity(Interface):
    pass


class ISerchableEntity(Interface):
    pass


class IVersionableEntity(Interface):
    pass


class IDuplicableEntity(Interface):
    pass


class ISerchableEntity(Interface):
    pass


class ICommentabl(Interface):
    pass


class IComment(ICommentabl):
    pass


class Iidea(ICommentabl,
            IDuplicableEntity,
            IVersionableEntity,
            ISerchableEntity,
            ICorrelableEntity):
    pass


class ICorrelation(ICommentabl):
    pass


class IInvitation(Interface):
    pass


class IKeyword(Interface):
    pass


class ICandidacy(Interface):
    pass


class IToken(Interface):
    pass


class IPerson(ISerchableEntity,
              ICorrelableEntity):
    pass


class IProposal(ICommentabl,
                ISerchableEntity,
                ICorrelableEntity):
    pass


class IWorkingGroup(Interface):
    pass


class IOrganization(Interface):
    pass


class INovaIdeoApplication(Interface):
    pass
