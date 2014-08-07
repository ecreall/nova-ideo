from zope.interface import Interface


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


class Iidea(ICommentabl):
    pass


class IInvitation(Interface):
    pass


class IKeyword(Interface):
    pass


class ICandidacy(Interface):
    pass


class IToken(Interface):
    pass


class IPerson(Interface):
    pass


class IProposal(ICommentabl):
    pass


class IWorkingGroup(Interface):
    pass


class IOrganization(Interface):
    pass


class INovaIdeoApplication(Interface):
    pass


