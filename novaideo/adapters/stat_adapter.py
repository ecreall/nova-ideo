# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import types
from zope.interface import Interface, implementer
from pyramid import renderers
from dace.util import Adapter, adapter, find_catalog

from novaideo import _
from novaideo.content.interface import (
    IChallenge,
    Iidea,
    IProposal,
    IQuestion,
    IPerson,
    IOrganization,
    INovaIdeoApplication)


DEFAULT_STAT_TEMPLATE = 'novaideo:views/templates/entity_stats.pt'

DEFAULT_EVALUATION_STAT_TEMPLATE = 'novaideo:views/templates/entity_stats_chart.pt'

SUPPORT_COLOR = '#2ea88d'

OPPOSE_COLOR = '#de6819'

EXAMINATION_VALUES = {
    'favorable': {'title':_('Positive'), 'color': '#40b322'},
    'to_study': {'title':_('To be re-worked upon'), 'color': '#f1a02d'},
    'unfavorable': {'title':_('Negative'), 'color': '#f13b2d'}
}


class IStat(Interface):

    def get_content_stat(request):
        pass

    def get_evaluation_stat(request):
        pass

    def get_examination_stat(request):
        pass

    def render_stat(request, template=DEFAULT_STAT_TEMPLATE, data=None):
        pass

    def render_evaluation_stat(
        request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        pass

    def render_examination_stat(
        request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
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

    def get_evaluation_stat(self, request):
        return None

    def render_stat(self, request, template=DEFAULT_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_content_stat(request)
        return renderers.render(
            template,
            data,
            request)

    def render_evaluation_stat(
        self, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        return None

    def render_examination_stat(
        self, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        return None


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

    def get_evaluation_stat(self, request):
        return None

    def render_stat(self, request, template=DEFAULT_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_content_stat(request)
        return renderers.render(
            template,
            data,
            request)

    def render_evaluation_stat(
        self, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        return None

    def render_examination_stat(
        self, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        return None


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

    def get_evaluation_stat(self, request):
        novaideo_index = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        organizations_index = novaideo_index['organizations']
        query = organizations_index.any([self.context.__oid__])
        objects = query.execute()
        support = novaideo_index['support']
        oppose = novaideo_index['oppose']
        intersection = organizations_index.family.IF.intersection
        object_ids = getattr(objects, 'ids', objects)
        if isinstance(object_ids, (list, types.GeneratorType)):
            object_ids = organizations_index.family.IF.Set(object_ids)
        # calculate sum of support / sum of opposition
        support_nb = 0
        for nb, supportoids in support._fwd_index.items():
            if nb > 0:
                support_nb += nb * len(intersection(supportoids, object_ids))

        oppose_nb = 0
        for nb, opposeoids in oppose._fwd_index.items():
            if nb > 0:
                oppose_nb += nb * len(intersection(opposeoids, object_ids))

        localizer = request.localizer
        items = {
            'support': {
                'value': support_nb,
                'color': SUPPORT_COLOR,
                'translation': localizer.translate(_('Support', context='analytics'))
            },
            'opposition': {
                'value': oppose_nb,
                'color': OPPOSE_COLOR,
                'translation': localizer.translate(_('Opposition'))
            }
        }

        return items

    def get_examination_stat(self, request):
        novaideo_index = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        organizations_index = novaideo_index['organizations']
        object_keywords = novaideo_index['object_keywords']
        items = {}
        localizer = request.localizer
        for examination, data in EXAMINATION_VALUES.items():
            query = organizations_index.any([self.context.__oid__]) & \
                states_index.any([examination])
            items[examination] = {
                'value': len(query.execute()),
                'color': data['color'],
                'translation': localizer.translate(data['title'])
            }

        return items

    def render_stat(self, request, template=DEFAULT_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_content_stat(request)
        return renderers.render(
            template,
            data,
            request)

    def render_evaluation_stat(
        self, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_evaluation_stat(request)
        
        result = {
          'object': self.context,
          'items': data,
          'sum': sum([values['value'] for _, values in data.items()]),
          'id': 'evaluation',
          'title': request.localizer.translate(_('Evaluations'))}
        return renderers.render(
            template,
            result,
            request) if data else None


    def render_examination_stat(
        self, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_examination_stat(request)
        
        result = {
          'object': self.context,
          'items': data,
          'sum': sum([values['value'] for _, values in data.items()]),
          'id': 'examination',
          'title': request.localizer.translate(_('Examinations'))}
        return renderers.render(
            template,
            result,
            request) if data else None


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

    def get_evaluation_stat(self, request):
        novaideo_index = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        authors = novaideo_index['object_authors']
        query = authors.any([self.context.__oid__])
        objects = query.execute()
        support = novaideo_index['support']
        oppose = novaideo_index['oppose']
        intersection = authors.family.IF.intersection
        object_ids = getattr(objects, 'ids', objects)
        if isinstance(object_ids, (list, types.GeneratorType)):
            object_ids = authors.family.IF.Set(object_ids)
        # calculate sum of support / sum of opposition
        support_nb = 0
        for nb, supportoids in support._fwd_index.items():
            if nb > 0:
                support_nb += nb * len(intersection(supportoids, object_ids))

        oppose_nb = 0
        for nb, opposeoids in oppose._fwd_index.items():
            if nb > 0:
                oppose_nb += nb * len(intersection(opposeoids, object_ids))

        localizer = request.localizer
        items = {
            'support': {
                'value': support_nb,
                'color': SUPPORT_COLOR,
                'translation': localizer.translate(_('Support', context='analytics'))
            },
            'opposition': {
                'value': oppose_nb,
                'color': OPPOSE_COLOR,
                'translation': localizer.translate(_('Opposition'))
            }
        }

        return items

    def get_examination_stat(self, request):
        novaideo_index = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        authors = novaideo_index['object_authors']
        object_keywords = novaideo_index['object_keywords']
        items = {}
        localizer = request.localizer
        for examination, data in EXAMINATION_VALUES.items():
            query = authors.any([self.context.__oid__]) & \
                states_index.any([examination])
            items[examination] = {
                'value': len(query.execute()),
                'color': data['color'],
                'translation': localizer.translate(data['title'])
            }

        return items

    def render_stat(self, request, template=DEFAULT_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_content_stat(request)
        return renderers.render(
            template,
            data,
            request)

    def render_evaluation_stat(
        self, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_evaluation_stat(request)
        
        result = {
          'object': self.context,
          'items': data,
          'sum': sum([values['value'] for _, values in data.items()]),
          'id': 'evaluation',
          'title': request.localizer.translate(_('Evaluations'))}
        return renderers.render(
            template,
            result,
            request) if data else None

    def render_examination_stat(
        self, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE, data=None):
        if data is None:
            data = self.get_examination_stat(request)
        
        result = {
          'object': self.context,
          'items': data,
          'sum': sum([values['value'] for _, values in data.items()]),
          'id': 'examination',
          'title': request.localizer.translate(_('Examinations'))}
        return renderers.render(
            template,
            result,
            request) if data else None