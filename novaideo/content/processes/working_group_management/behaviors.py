# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.httpexceptions import HTTPFound

from dace.processinstance.activity import InfiniteCardinality

from novaideo.content.interface import IWorkingGroup


def edit_relation_validation(process, context):
    return True


def edit_roles_validation(process, context):
    return True


def edit_processsecurity_validation(process, context):
    return True


def edit_state_validation(process, context):
    return True


class EditAction(InfiniteCardinality):
    isSequential = True
    context = IWorkingGroup
    relation_validation = edit_relation_validation
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors
