# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.objectofcollaboration.principal.util import (
    get_current)
from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.content.processes.novaideo_view_manager.behaviors import SeeBallot
from novaideo.content.ballot import Ballot
from novaideo.utilities.util import (
    render_listing_objs)
from novaideo import _, log
from novaideo.content.novaideo_application import NovaIdeoApplication


BATCH_DEFAULT_SIZE = 20


CONTENTS_MESSAGES = {
    '0': _(u"""No vote"""),
    '1': _(u"""One vote"""),
    '*': _(u"""${nember} votes""")
}


@view_config(
    name='seevotes',
    context=Ballot,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class VotesView(BasicView):
    name = 'seevotes'
    viewid = 'seevotes'
    template = 'novaideo:views/novaideo_view_manager/templates/table_result.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    view_icon = 'glyphicon glyphicon-inbox'
    title = _('Votes')
    empty_message = _("No vote")
    empty_icon = 'glyphicon glyphicon-saved'
    selected_filter = [('temporal_filter', ['negation', 'created_date']),
                       'text_filter']

    def update(self):
        user = get_current()
        context = self.get_binding('context')
        context = context if context else self.context
        result = {}
        body = ''
        if isinstance(context, Ballot):
            # Vote is non a searchable element
            objects = context.ballot_box.votes
            url = self.request.resource_url(context, self.name)
            batch = Batch(objects, self.request,
                          url=url,
                          default_size=BATCH_DEFAULT_SIZE)
            batch.target = "#results-votes"
            len_votes = batch.seqlen
            index = str(len_votes) if len_votes <= 1 else '*'
            if not self.parent:
                self.title = _(CONTENTS_MESSAGES[index],
                               mapping={'nember': len_votes})
            elif index != '*':
                self.title = _('The vote')

            result_body, result = render_listing_objs(
                self.request, batch, user)
            values = {'bodies': result_body,
                      'batch': batch,
                      'empty_message': self.empty_message,
                      'empty_icon': self.empty_icon}
            body = self.content(args=values, template=self.template)['body']

        item = self.adapt_item(body, self.viewid)
        item['isactive'] = True
        result['coordinates'] = {self.coordinates: [item]}
        return result


class BallotresultView(BasicView):
    name = 'seeballotresultballot'
    viewid = 'seeballotresultballot'
    template = 'novaideo:views/novaideo_view_manager/templates/ballotresult.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    view_icon = 'glyphicon glyphicon-stats'
    title = _('The result of the ballot')
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/chartjs/Chart.js',
                                 'novaideo:static/js/analytics.js']}

    def update(self):
        result = {}
        context = self.get_binding('context')
        if context.is_finished:
            ballot_type = context.report.ballottype
            values = {
                'ballot': context,
                'ballot_type': ballot_type,
                'tab_id': self.viewid + self.coordinates
            }
            ballot_type_body = self.content(
                args=values,
                template=ballot_type.templates.get('result'))['body']
            values = {'body': ballot_type_body,
                      'ballot': context}
            body = self.content(
                args={'body': ballot_type_body,
                      'ballot': context}, template=self.template)['body']
        else:
            values = {'body': '',
                      'ballot': context}

        body = self.content(
            args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        result = merge_dicts(self.requirements_copy, result)
        return result


class VotesDetailsView(MultipleView):
    name = 'seevotesdetails'
    viewid = 'seevotesdetails'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    css_class = 'integreted-tab-content ballot-details'
    title = ''
    views = (VotesView, BallotresultView)

    def _activate(self, items):
        pass


class SeeBallotHeaderView(BasicView):
    title = ''
    name = 'seeballotheader'
    behaviors = [SeeBallot]
    template = 'novaideo:views/novaideo_view_manager/templates/see_ballot.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    viewid = 'seeballotheader'

    def update(self):
        self.execute(None)
        user = get_current()
        context = self.get_binding('context')
        votes = context.ballot_box.votes
        len_votes = len(votes)
        index = str(len_votes)
        if len_votes > 1:
            index = '*'

        votes_title = _(CONTENTS_MESSAGES[index],
                        mapping={'nember': len_votes})
        result = {}
        ballot_type = context.report.ballottype
        values = {
            'ballot': context,
            'ballot_type': ballot_type,
            'current_user': user,
            'votes_title': votes_title,
        }
        ballot_type_body = self.content(
            args=values, template=ballot_type.templates.get('detail'))['body']
        body = self.content(
            args={'body': ballot_type_body}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@view_config(
    name='seeballot',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeBallotView(MultipleView):
    name = 'seeballot'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    title = ''
    container_css_class = 'ballot-view-container'
    views = (SeeBallotHeaderView, VotesDetailsView)
    validators = [SeeBallot.get_validator()]

    def update(self):
        context = self.get_binding('context')
        if isinstance(context, Ballot):
            return super(SeeBallotView, self).update()

        result = {}
        item = self.adapt_item('', self.viewid)
        item['isactive'] = True
        result['coordinates'] = {self.coordinates: [item]}
        return result

    def bind(self):
        bindings = {}
        ballot_id = self.params('id')
        context = None
        try:
            context = get_obj(int(ballot_id))
        except Exception as error:
            log.warning(error)

        bindings['context'] = context
        setattr(self, '_bindings', bindings)


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeBallot: SeeBallotView})
