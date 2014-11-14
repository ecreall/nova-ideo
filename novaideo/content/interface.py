from zope.interface import Interface


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


class ISearchableEntity(Interface):
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


class INovaIdeoApplication(Interface):
    pass
