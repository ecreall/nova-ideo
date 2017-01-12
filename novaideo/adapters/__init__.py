# -*- coding: utf8 -*-
# Copyright (c) 2016 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from zope.interface import Interface, implementer

from dace.util import Adapter, adapter

from novaideo.content.interface import (
    IEntity,
    IPerson)
from novaideo import _
from novaideo.content.processes import get_states_mapping

null_value = 'null'

EXTRACTION_ATTR = {
    'type': {'title': _('Type'), 'order': 0},
    'title': {'title': _('Title'), 'order': 1},
    'state': {'title': _('State'), 'order': 2},
    'author': {'title': _('Author'), 'order': 3},
    'email': {'title': _('Email'), 'order': 4},
    'keywords': {'title': _('Keywords'), 'order': 5},
    'description': {'title': _('Description'), 'order': 6},
    'organization': {'title': _('Organization'), 'order': 7},
    'created_at': {'title': _('Created on'), 'order': 8},
    'modified_at': {'title': _('Modified on'), 'order': 9},
    'examined_at': {'title': _('Examined on'), 'order': 10},
    'published_at': {'title': _('Published on'), 'order': 11},
    'content': {'title': _('Content'), 'order': 12},
}


class IExtractionAdapter(Interface):

    def type(user, request):
        pass

    def title(user, request):
        pass

    def state(user, request):
        pass

    def keywords(user, request):
        pass

    def description(user, request):
        pass

    def content(user, request):
        pass

    def organization(user, request):
        pass

    def author(user, request):
        pass

    def email(user, request):
        pass

    def created_at(user, request):
        pass

    def modified_at(user, request):
        pass

    def published_at(user, request):
        pass

    def examined_at(user, request):
        pass


@adapter(context=IEntity)
@implementer(IExtractionAdapter)
class ExtractionAdapter(Adapter):
    """Return all keywords.
    """
    def type(self, user, request):
        return getattr(self.context, 'type_title', null_value)

    def title(self, user, request):
        return getattr(self.context, 'title', null_value)

    def state(self, user, request):
        states = getattr(self.context, 'state', [])
        result = []
        for state in states:
            result.append(request.localizer.translate(
                get_states_mapping(
                    None, self.context, state)))

        return ', '.join(result)

    def keywords(self, user, request):
        keywords = ','.join(list(getattr(self.context, 'keywords', [])))
        return keywords if keywords else null_value

    def author(self, user, request):
        author = getattr(self.context, 'author', None)
        if author:
            return getattr(author, 'title', null_value)

        return null_value

    def organization(self, user, request):
        author = getattr(self.context, 'author', None)
        organization = getattr(author, 'organization', None)
        if organization:
            return organization.title

        return null_value

    def email(self, user, request):
        return null_value

    def created_at(self, user, request):
        return getattr(self.context, 'created_at', null_value)

    def modified_at(self, user, request):
        return getattr(self.context, 'modified_at', null_value)

    def published_at(self, user, request):
        return getattr(
        	self.context, 'published_at', self.created_at(user, request))

    def examined_at(self, user, request):
        return getattr(self.context, 'examined_at', null_value)

    def description(self, user, request):
        return getattr(self.context, 'description', null_value)

    def content(self, user, request):
        return getattr(self.context, 'text', null_value)


@adapter(context=IPerson)
@implementer(IExtractionAdapter)
class PersonExtraction(ExtractionAdapter):

    def author(self, user, request):
        return self.context.title

    def organization(self, user, request):
        organization = getattr(self.context, 'organization', None)
        if organization:
            return organization.title

        return null_value

    def email(self, user, request):
        return getattr(self.context, 'email', null_value)

    def content(self, user, request):
        return null_value
