# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeOrderedProposal)
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES, merge_with_filter_view, find_entities)


CONTENTS_MESSAGES = {
    '0': _(u"""No proposal found"""),
    '1': _(u"""One proposal found"""),
    '*': _(u"""${nember} proposals found""")
    }


def sort_proposals(proposals):
    ordered_proposals = [(proposal,
                          (len(proposal.tokens_support) - \
                           len(proposal.tokens_opposition))) \
                         for proposal in proposals]
    groups = {}
    for proposal in ordered_proposals:
        if groups.get(proposal[1], None):
            groups[proposal[1]].append(proposal)
        else:
            groups[proposal[1]] = [proposal]

    for group_key in list(groups.keys()):
        sub_proposals = list(groups[group_key])
        groups[group_key] = sorted(sub_proposals,
                    key=lambda proposal: len(proposal[0].tokens_support),
                    reverse=True)

    groups = sorted(groups.items(), key=lambda value: value[0], reverse=True)
    return [proposal[0] for sublist in groups \
           for proposal in sublist[1]]


@view_config(
    name='proposalstoexamine',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeOrderedProposalView(BasicView):
    title = _('Proposals to examine')
    name = 'proposalstoexamine'
    behaviors = [SeeOrderedProposal]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'proposalstoexamine'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def _add_filter(self, user):
        def source(**args):
            filters = [
                {'metadata_filter': {
                    'content_types': ['proposal'],
                    'states': ['submitted_support']
                }}
            ]
            objects = find_entities(
                user=user, include_site=True, filters=filters, **args)
            return objects

        url = self.request.resource_url(self.context, '@@novaideoapi')
        return get_filter(
            self,
            url=url,
            source=source,
            select=[('metadata_filter', ['keywords']),
                    'contribution_filter',
                    ('temporal_filter', ['negation', 'created_date']),
                    'text_filter', 'other_filter'])

    def update(self):
        self.execute(None)
        user = get_current()
        filter_form, filter_data = self._add_filter(user)
        filters = [
            {'metadata_filter': {
                'content_types': ['proposal'],
                'states': ['submitted_support']
            }}
        ]
        args = {}
        args = merge_with_filter_view(self, args)
        args['request'] = self.request
        objects = find_entities(
            user=user,
            filters=filters,
            **args)
        if 'proposal' in self.request.content_to_support:
            objects = sort_proposals(objects)

        url = self.request.resource_url(self.context, 'proposalstoexamine')
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_contents"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})
        filter_data['filter_message'] = self.title
        filter_body = self.filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
        if filter_form:
            result = merge_dicts(
                {'css_links': filter_form['css_links'],
                 'js_links': filter_form['js_links']
                }, result)

        values = {'bodies': result_body,
                  'batch': batch,
                  'filter_body': filter_body}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeOrderedProposal: SeeOrderedProposalView})


FILTER_SOURCES.update(
    {SeeOrderedProposalView.name: SeeOrderedProposalView})
