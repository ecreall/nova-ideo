# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from zope.interface import Interface, implementer
from pyramid import renderers

from dace.util import Adapter, adapter, find_catalog

from novaideo.content.interface import (
    IChallenge,
    Iidea,
    IProposal,
    IQuestion,
    IPerson,
    IOrganization,
    INovaIdeoApplication)


DEFAULT_STAT_TEMPLATE = 'novaideo:views/templates/entity_stats.pt'


class IStat(Interface):

    def get_content_stat(request):
        pass

    def render_stat(request, template=DEFAULT_STAT_TEMPLATE, data=None):
        pass


@adapter(context=INovaIdeoApplication)
@implementer(IStat)
class ApplicationAdapter(Adapter):
    """Return Person stats.
    """
    def get_content_stat(self, request):
        result = {}
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any((IPerson.__identifier__,)) & \
            states_index.notany(['deactivated'])
        result['nb_user'] = query.execute().__len__()
        query = object_provides_index.any((Iidea.__identifier__,)) & \
            states_index.any(['published'])
        result['nb_idea'] = query.execute().__len__()
        result['nb_question'] = 0
        if 'question' in request.content_to_manage:
            query = object_provides_index.any((IQuestion.__identifier__,)) & \
                states_index.any(['published'])
            result['nb_question'] = query.execute().__len__()

        result['nb_proposal'] = 0
        if 'proposal' in request.content_to_manage:
            query = object_provides_index.any((IProposal.__identifier__,)) & \
                states_index.notany(['archived', 'draft', 'submitted'])
            result['nb_proposal'] = query.execute().__len__()

        return result

    def render_stat(self, request, template=DEFAULT_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_content_stat(request)
        return renderers.render(
            template,
            data,
            request)


@adapter(context=IChallenge)
@implementer(IStat)
class ChallengeAdapter(Adapter):
    """Return Challenge stats.
    """
    def get_content_stat(self, request):
        result = {}
        novaideo_index = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        challenges = novaideo_index['challenges']
        query = challenges.any([self.context.__oid__]) & \
            object_provides_index.any((Iidea.__identifier__,)) & \
            states_index.any(['published'])
        result['nb_idea'] = query.execute().__len__()
        result['nb_question'] = 0
        if 'question' in request.content_to_manage:
            query = challenges.any([self.context.__oid__]) & \
                object_provides_index.any((IQuestion.__identifier__,)) & \
                states_index.any(['published'])
            result['nb_question'] = query.execute().__len__()

        result['nb_proposal'] = 0
        if 'proposal' in request.content_to_manage:
            query = challenges.any([self.context.__oid__]) & \
                object_provides_index.any((IProposal.__identifier__,)) & \
                states_index.notany(['archived', 'draft'])
            result['nb_proposal'] = query.execute().__len__()

        return result

    def render_stat(self, request, template=DEFAULT_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_content_stat(request)
        return renderers.render(
            template,
            data,
            request)


@adapter(context=IOrganization)
@implementer(IStat)
class OrganizationAdapter(Adapter):
    """Return organization stats.
    """
    def get_content_stat(self, request):
        result = {}
        novaideo_index = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        organizations_index = novaideo_index['organizations']
        query = organizations_index.any([self.context.__oid__]) & \
            object_provides_index.any((IPerson.__identifier__,)) & \
            states_index.any(['active'])
        result['nb_user'] = query.execute().__len__()
        query = organizations_index.any([self.context.__oid__]) & \
            object_provides_index.any((Iidea.__identifier__,)) & \
            states_index.any(['published'])
        result['nb_idea'] = query.execute().__len__()
        result['nb_question'] = 0
        if 'question' in request.content_to_manage:
            query = organizations_index.any([self.context.__oid__]) & \
                object_provides_index.any((IQuestion.__identifier__,)) & \
                states_index.any(['published'])
            result['nb_question'] = query.execute().__len__()

        result['nb_proposal'] = 0
        if 'proposal' in request.content_to_manage:
            query = organizations_index.any([self.context.__oid__]) & \
                object_provides_index.any((IProposal.__identifier__,)) & \
                states_index.notany(['archived', 'draft'])
            result['nb_proposal'] = query.execute().__len__()

        return result

    def render_stat(self, request, template=DEFAULT_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_content_stat(request)
        return renderers.render(
            template,
            data,
            request)


@adapter(context=IPerson)
@implementer(IStat)
class PersonAdapter(Adapter):
    """Return Person stats.
    """
    def get_content_stat(self, request):
        result = {}
        novaideo_index = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        authors = novaideo_index['object_authors']
        query = authors.any([self.context.__oid__]) & \
            object_provides_index.any((Iidea.__identifier__,)) & \
            states_index.any(['published'])
        result['nb_idea'] = query.execute().__len__()
        result['nb_question'] = 0
        if 'question' in request.content_to_manage:
            query = authors.any([self.context.__oid__]) & \
                object_provides_index.any((IQuestion.__identifier__,)) & \
                states_index.any(['published'])
            result['nb_question'] = query.execute().__len__()

        result['nb_proposal'] = 0
        if 'proposal' in request.content_to_manage:
            query = authors.any([self.context.__oid__]) & \
                object_provides_index.any((IProposal.__identifier__,)) & \
                states_index.notany(['archived', 'draft'])
            result['nb_proposal'] = query.execute().__len__()

        query = authors.any([self.context.__oid__]) & \
            object_provides_index.notany(
                (Iidea.__identifier__, IQuestion.__identifier__, IProposal.__identifier__)) & \
            states_index.any(['published'])
        result['nb_other'] = query.execute().__len__()
        return result

    def render_stat(self, request, template=DEFAULT_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_content_stat(request)
        return renderers.render(
            template,
            data,
            request)
