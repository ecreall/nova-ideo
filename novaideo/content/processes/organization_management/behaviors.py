from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import has_any_roles
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep,
    ActionType)
from novaideo.ips.xlreader import creat_object_from_xl
from novaideo.content.interface import INovaIdeoApplication, IOrganization
from novaideo.content.organization import Organization
from novaideo import _


def add_relation_validation(process, context):
    return True


def add_roles_validation(process, context):
    return has_any_roles(roles=('Moderator',)) 


def add_processsecurity_validation(process, context):
    return True


def add_state_validation(process, context):
    return True


class AddOrganizations(InfiniteCardinality):
    isSequential = True
    context = INovaIdeoApplication
    relation_validation = add_relation_validation
    roles_validation = add_roles_validation
    processsecurity_validation = add_processsecurity_validation
    state_validation = add_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        xlfile = appstruct['file']['_object_data']
        organizations = creat_object_from_xl(file=xlfile, factory=Organization, properties={'title':('String', False),
                                                                                            'description':('String', False)})
        root.setproperty('organizations', organizations)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def creatorg_relation_validation(process, context):
    return True


def creatorg_roles_validation(process, context):
    return has_any_roles(roles=('Moderator',)) 


def creatorg_processsecurity_validation(process, context):
    return True


def creatorg_state_validation(process, context):
    return True


class CreatOrganizations(InfiniteCardinality):
    isSequential = True
    context = INovaIdeoApplication
    relation_validation = creatorg_relation_validation
    roles_validation = creatorg_roles_validation
    processsecurity_validation = creatorg_processsecurity_validation
    state_validation = creatorg_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        new_organizations = appstruct['organizations']
        for organization_dict in new_organizations:
            organization = organization_dict['_object_data'] 
            root.addtoproperty('organizations', organization)
            #send mail
    
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def edit_relation_validation(process, context):
    return True


def edit_roles_validation(process, context):
    return has_any_roles(roles=('Moderator',)) 


def edit_processsecurity_validation(process, context):
    return len(context.organizations)>=1


def edit_state_validation(process, context):
    return True


class EditOrganizations(InfiniteCardinality):
    isSequential = True
    context = INovaIdeoApplication
    relation_validation = edit_relation_validation
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seeorgs_relation_validation(process, context):
    return True


def seeorgs_roles_validation(process, context):
    return has_any_roles(roles=('Collaborator',)) 


def seeorgs_processsecurity_validation(process, context):
    return len(context.organizations)>=1


def seeorgs_state_validation(process, context):
    return True


class SeeOrganizations(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    relation_validation = seeorgs_relation_validation
    roles_validation = seeorgs_roles_validation
    processsecurity_validation = seeorgs_processsecurity_validation
    state_validation = seeorgs_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def see_relation_validation(process, context):
    return True


def see_roles_validation(process, context):
    return has_any_roles(roles=('Collaborator',)) 


def see_processsecurity_validation(process, context):
    return True


def see_state_validation(process, context):
    return True


class SeeOrganization(InfiniteCardinality):
    isSequential = False
    title = _('Details')
    actionType = ActionType.automatic
    context = IOrganization
    relation_validation = see_relation_validation
    roles_validation = see_roles_validation
    processsecurity_validation = see_processsecurity_validation
    state_validation = see_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def editorg_relation_validation(process, context):
    return True


def editorg_roles_validation(process, context):
    return has_any_roles(roles=('Moderator',)) 


def editorg_processsecurity_validation(process, context):
    return True


def editorg_state_validation(process, context):
    return True


class EditOrganization(InfiniteCardinality):
    isSequential = False
    title = _('Edit organization')
    context = IOrganization
    relation_validation = editorg_relation_validation
    roles_validation = editorg_roles_validation
    processsecurity_validation = editorg_processsecurity_validation
    state_validation = editorg_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))
#TODO bihaviors
