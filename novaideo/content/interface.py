from zope.interface import Interface


class ICorrelableEntity(Interface):
    pass


class ISearchableEntity(Interface):
    pass


class IVersionableEntity(Interface):
    pass


class IDuplicableEntity(Interface):
    pass


class ISearchableEntity(Interface):
    pass


class ICommentable(Interface):
    pass


class IComment(ICommentable):
    pass


class Iidea(ICommentable,
            IDuplicableEntity,
            IVersionableEntity,
            ISearchableEntity,
            ICorrelableEntity):
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


class IProposal(ICommentable,
                ISearchableEntity,
                ICorrelableEntity):
    pass


class IWorkingGroup(Interface):
    pass


class IOrganization(Interface):
    pass


class INovaIdeoApplication(Interface):
    pass
