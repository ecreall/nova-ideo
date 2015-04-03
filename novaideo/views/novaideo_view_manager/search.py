# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import re
import colander
import datetime
from collections import OrderedDict
from pyramid.view import view_config

from substanced.util import Batch, get_oid

from dace.util import find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from dace.objectofcollaboration.entity import Entity
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.widget import CheckboxChoiceWidget
from pontus.schema import Schema
from pontus.form import FormView

from novaideo.content.processes.novaideo_view_manager.behaviors import  Search
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.content.interface import (
    Iidea, 
    IProposal, 
    IPerson, 
    ICorrelableEntity)
from .widget import SearchTextInputWidget, SearchFormWidget
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.core import can_access
from novaideo.content.processes import get_states_mapping


_SEARCHABLE_CONTENT_ORDER = {'Idea': 1, 
                             'Proposal': 2, 
                             'Person': 3}

SEARCHABLE_CONTENT_TITLE = {'Idea': _('Ideas'),
                            'Proposal': _('Proposals'),
                            'Person': _('Persons')
                           }

DEFAULT_SEARCHABLE_CONTENT = {'Idea': Iidea,
                              'Proposal': IProposal,
                              'Person': IPerson
                            }

SEARCHABLE_CONTENT = {'Idea': Iidea,
                      'Proposal': IProposal,
                      'Person': IPerson,
                      'CorrelableEntity': ICorrelableEntity,
                    } 

@colander.deferred
def content_types_choices(node, kw):
    values = [(k, SEARCHABLE_CONTENT_TITLE.get(k, k)) for k \
              in DEFAULT_SEARCHABLE_CONTENT]
    values = sorted(values, \
                key=lambda v: _SEARCHABLE_CONTENT_ORDER.get(v[0], 100))
    return CheckboxChoiceWidget(values=values, inline=True)


@colander.deferred
def default_content_types_choices(node, kw):
    return sorted(DEFAULT_SEARCHABLE_CONTENT.keys())


class SearchSchema(Schema):
    widget = SearchFormWidget()

    content_types = colander.SchemaNode(
                colander.Set(),
                widget=content_types_choices, 
                title='',
                default=default_content_types_choices,
                missing=default_content_types_choices,
                )

    text_to_search = colander.SchemaNode(
        colander.String(),
        widget=SearchTextInputWidget(
            button_type='submit',
            description=_("The keyword search is done using"
                          " commas between keywords.")),
        title='',
        missing='',
        )


@view_config(
    name='search',
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SearchView(FormView):
    title = _('Search')
    name = 'search'
    coordinates = 'header'
    schema = SearchSchema()
    behaviors = [Search]
    formid = 'formsearch'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'

    def get_appstruct(self):
        post = getattr(self, 'postedform', self.request.POST)
        form, reqts = self._build_form()
        form.formid = self.viewid + '_' + form.formid
        posted_formid = None
        default_content = list(DEFAULT_SEARCHABLE_CONTENT.keys())
        default_content.remove("Person")
        if '__formid__' in post:
            posted_formid = post['__formid__']

        if posted_formid is not None and posted_formid == form.formid:
            try:
                post = post.copy()
                controls = post.items()
                validated = form.validate(controls)
                if 'content_types' in validated:
                    return validated
                else:
                    validated['content_types'] = default_content
                    return validated
            except Exception:
                pass

        content_types = self.params('content_types')
        text = self.params('text_to_search')
        if text is None:
            text = ''

        if content_types is None:
            content_types = default_content
        elif not isinstance(content_types, (list, tuple)):
            content_types = [content_types]

        return {'content_types':content_types, 'text_to_search':text} 

    def before_update(self):
        root = getSite()
        self.action = self.request.resource_url(root, '')

    def default_data(self):
        appstruct = self.get_appstruct()
        return appstruct

def search(text, content_types, user):
    if text:
        text = [t.lower() for t in re.split(', *', text)]

    interfaces = [SEARCHABLE_CONTENT[i].__identifier__ for i in content_types]
    #catalog
    dace_catalog = find_catalog('dace')
    novaideo_catalog = find_catalog('novaideo')
    system_catalog = find_catalog('system')
    #index
    title_index = dace_catalog['object_title']
    description_index = dace_catalog['object_description']
    states_index = dace_catalog['object_states']
    object_provides_index = dace_catalog['object_provides']
    keywords_index = novaideo_catalog['object_keywords']
    text_index = system_catalog['text']
    name_index = system_catalog['name']
    #query
    query = None
    if text:
        query = keywords_index.any(text) | \
                name_index.any(text) | \
                states_index.any(text)

        for keyword in text:
            query = query | \
                    title_index.contains(keyword) | \
                    description_index.contains(keyword) | \
                    text_index.contains(keyword)

    if query is None:
        query = object_provides_index.any(interfaces)
    else:
        query = (query) & object_provides_index.any(interfaces)

    query = (query) & states_index.notany(('archived',)) 
    resultset = query.execute()
    objects = [o for o in resultset.all() if can_access(user, o)] 
    objects = sorted(objects, 
                      key=lambda e: getattr(e, 'modified_at',
                                            datetime.datetime.today()),
                     reverse=True)
    return objects


CONTENTS_MESSAGES = {
        '0': _(u"""No element found"""),
        '1': _(u"""One element found"""),
        '*': _(u"""${nember} elements found""")
                        }


@view_config(
    name='',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SearchResultView(BasicView):
    title = _('Nova-Ideo contents')
    name = ''
    validators = [Search.get_validator()]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'search_result'

    def update(self):
        user = get_current()
        formviewinstance = SearchView(self.context, self.request)
        formviewinstance.postedform = self.request.POST
        appstruct = formviewinstance.get_appstruct()
        content_types = appstruct['content_types']
        text = appstruct['text_to_search']
        objects = search(text, content_types, user)
        url = self.request.resource_url(self.context, '', 
                                        query={'content_types':content_types,
                                               'text_to_search':appstruct['text_to_search']})
        batch = Batch(objects, 
                      self.request, 
                      url=url, 
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index] , 
                       mapping={'nember': len_result})
        result_body = []
        for obj in batch:
            object_values = {'object':obj, 
                             'current_user': user, 
                             'state': get_states_mapping(user, obj, 
                                   getattr(obj, 'state', [None])[0])}
            body = self.content(result=object_values,
                                template=obj.result_template)['body']
            result_body.append(body)

        result = {}
        values = {
                'bodies': result_body,
                'length': len_result,
                'batch': batch
                 }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        result  = merge_dicts(self.requirements_copy, result)
        return result


@view_config(name='search',
             context=Entity,
             xhr=True,
             renderer='json')
class Search_Json(BasicView):

    def toselect(self):
        user = get_current()
        content_types = self.params('content_types')
        if not isinstance(content_types, (list, tuple)):
            content_types = [content_types]

        text = self.params('text_to_search')
        objects = search(text, content_types, user)
        result = {'': _('- Select -')}
        result.update(dict([(get_oid(obj), obj.title) for obj in objects]))
        return result


    def find_entities(self):
        user = get_current()
        content_types = self.params('content_types')
        if not isinstance(content_types, (list, tuple)):
            content_types = [content_types]

        text = self.params('q')
        entries = search(text, content_types, user)
        result = {'items': [], 'total_count': len(entries)}
        result['items'] = [{'text': obj.title, 
                            'id': str(get_oid(obj)),
                            'icon': getattr(obj, 'icon', 
                                     'glyphicon glyphicon-question-sign')} \
                            for obj in entries]
        return result

    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({Search:SearchView})

