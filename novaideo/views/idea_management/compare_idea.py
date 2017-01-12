# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

import html_diff_wrapper
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import get_obj
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import CheckboxChoiceWidget, RadioChoiceWidget
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.file import Object as ObjectType

from novaideo.content.processes.idea_management.behaviors import CompareIdea
from novaideo.content.idea import Idea
from novaideo import _


COMPARE_MESSAGE = {'0': _(u"""No other version"""),
                   '1': _(u"""One available version"""),
                   '*': _(u"""${nember} available versions""")}


class DiffView(BasicView):

    title = _('Differences between versions')
    name = 'diffresult'
    viewid = 'diffresult'
    validators = [CompareIdea.get_validator()]
    template = 'novaideo:views/idea_management/templates/diff_result.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'

    #TODO current version
    def update(self):
        version = self.params('version')
        titlediff = ''
        textdiff = ''
        descriptiondiff = ''
        keywordsdiff = []
        versionobj = None
        if version is not None:
            versionobj = get_obj(int(version))
            soupt, textdiff = html_diff_wrapper.render_html_diff(
                getattr(versionobj, 'text', ''),
                getattr(self.context, 'text', ''))
            soupd, descriptiondiff = html_diff_wrapper.render_html_diff(
                '<div>'+getattr(versionobj, 'description', '')+'</div>',
                '<div>'+getattr(self.context, 'description', '')+'</div>')
            soupt, titlediff = html_diff_wrapper.render_html_diff(
                getattr(versionobj, 'title', ''),
                getattr(self.context, 'title', ''))
            for k in versionobj.keywords:
                if k in self.context.keywords:
                    keywordsdiff.append({'title': k, 'state': 'nothing'})
                else:
                    keywordsdiff.append({'title': k, 'state': 'del'})

            [keywordsdiff.append({'title': k, 'state': 'ins'})
             for k in self.context.keywords if k not in versionobj.keywords]

        result = {}
        values = {
            'version': versionobj,
            'idee': self.context,
            'textdiff': textdiff,
            'titlediff': titlediff,
            'descriptiondiff': descriptiondiff,
            'keywordsdiff': keywordsdiff
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@colander.deferred
def version_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    current_version = context.current_version
    values = [(i, i.get_view(request)) for i in current_version.history
              if i is not current_version]
    values = sorted(values, key=lambda v: v[0].modified_at, reverse=True)
    widget = RadioChoiceWidget(values=values)
    widget.template = 'novaideo:views/idea_management/templates/radio_choice.pt'
    return widget


class CompareIdeaSchema(Schema):

    versions = colander.SchemaNode(
        ObjectType(),
        widget=version_choice,
        title=_('Previous versions'),
        description=_("Select the previous version with which to compare"),
        missing=None
        )


class CompareIdeaFormView(FormView):

    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    title = _('Form to compare the idea')
    schema = select(CompareIdeaSchema(), ['versions'])
    behaviors = [CompareIdea]
    formid = 'formcompareidea'
    name = 'compareideaform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='compareform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget
        view_name = 'compare'
        formwidget.ajax_url = self.request.resource_url(self.context,
                                                        '@@'+view_name)


@view_config(
    name='compare',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CompareIdeaView(MultipleView):
    name = 'compare'
    view_icon = 'glyphicon glyphicon-time'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    css_class = 'compare-block'
    contextual_help = 'compare-help'
    title = _('Compare the versions')
    views = (CompareIdeaFormView, DiffView)
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/compare_idea.js']}

    def before_update(self):
        len_history = len(self.context.history) - 1
        index = str(len_history)
        if len_history > 1:
            index = '*'

        self.title = _(COMPARE_MESSAGE[index],
                       mapping={'nember': len_history})
        super(CompareIdeaView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CompareIdea: CompareIdeaView})
