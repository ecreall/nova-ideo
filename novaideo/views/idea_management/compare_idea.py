# -*- coding: utf8 -*-
import colander
import deform
from zope.interface import invariant
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from substanced.util import find_service

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, get_obj
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import CheckboxChoiceWidget, RadioChoiceWidget
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.file import  Object as ObjectType

from novaideo.content.processes.idea_management.behaviors import  CompareIdea
from novaideo.content.idea import Idea
from novaideo import _
from novaideo.utilities.text_analyzer import ITextAnalyzer


compare_message = {'0': u"""Pas de versions""",
                       '1': u"""Voir la version""",
                       '*': u"""Voir les {len_history} versions"""}


class DiffView(BasicView):

    title = _('Diff result')
    name = 'diffresult'
    viewid = 'diffresult'
    validators = [CompareIdea.get_validator()]
    template = 'novaideo:views/idea_management/templates/diff_result.pt'

    #TODO current version
    def update(self):
        version = self.params('version')
        textdiff = ''
        descriptiondiff = ''
        keywordsdiff = []
        versionobj = None
        if version is not None:
             versionobj = get_obj(int(version))
             text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
             soupt, textdiff =  text_analyzer.render_html_diff(getattr(versionobj, 'text', ''), getattr(self.context, 'text', ''))
             soupd, descriptiondiff = text_analyzer.render_html_diff('<div>'+getattr(versionobj, 'description', '')+'</div>', '<div>'+getattr(self.context, 'description', '')+'</div>')
             for k in versionobj.keywords:
                 if k in self.context.keywords:
                     keywordsdiff.append({'title':k,'state':'nothing'})
                 else:
                     keywordsdiff.append({'title':k,'state':'del'})
                  
             [keywordsdiff.append({'title':k,'state':'ins'}) for k in self.context.keywords if k not in versionobj.keywords]

        result = {}
        values = {
                'version' : versionobj,
                'idee': self.context,
                'textdiff': textdiff,
                'descriptiondiff':descriptiondiff,
                'keywordsdiff':keywordsdiff
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


@colander.deferred
def version_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    current_version = context.current_version
    values = [(i, i.get_view(request)) for i in current_version.history if not(i is current_version)]
    values = sorted(values, key=lambda v: v[0].modified_at, reverse=True) 
    widget = RadioChoiceWidget(values=values)
    widget.template = 'novaideo:views/idea_management/templates/radio_choice.pt'
    return widget


@colander.deferred
def current_version_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    current_version = context.current_version
    values = [(current_version, current_version.get_view(request))]
    return CheckboxChoiceWidget(values=values, multiple=True, readonly=True)


@colander.deferred
def default_current_version_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = [context.current_version]
    return values


class CompareIdeaSchema(Schema):

    current_version = colander.SchemaNode(
        colander.Set(),
        widget=current_version_choice,
        default=default_current_version_choice,
        missing=[],
        title=_('Current version')
        )

    versions = colander.SchemaNode(
        ObjectType(),
        widget=version_choice,
        title=_('Last versions')
        )
    

class CompareIdeaFormView(FormView):

    title = _('Compare idea form')
    schema = select(CompareIdeaSchema(), ['current_version', 'versions'])
    behaviors = [CompareIdea]
    formid = 'formcompareidea'
    name='compareideaform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='compareform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget
        view_name = 'compareidea'
        formwidget.ajax_url = self.request.resource_url(self.context, '@@'+view_name)


@view_config(
    name='compareidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class CompareIdeaView(MultipleView):
    title = _('Compare the idea')
    name='compareidea'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (CompareIdeaFormView, DiffView)

    def get_message(self):
        len_history = len(self.context.history)
        index = str(len_history)
        if len_history>1:
            index = '*'
        message = (compare_message[index]).format(len_history=len_history)
        return message


DEFAULTMAPPING_ACTIONS_VIEWS.update({CompareIdea:CompareIdeaView})
