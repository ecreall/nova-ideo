from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from novaideo.ips.xlreader import creat_object_from_xl
from novaideo.content.interface import INovaIdeoApplication
from novaideo.content.organization import Organization


def add_relation_validation(process, context):
    return True


def add_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


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
    return True#has_any_roles(roles=('Moderator',))


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
        import pdb; pdb.set_trace()
        new_organizations = appstruct['organizations']
        for organization_dict in new_organizations:
            organization = organization_dict['_object_data'] 
            root.addtoproperty('organizations', organization)
            #send mail
    
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO bihaviors
