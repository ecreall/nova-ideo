import re
import colander
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.util import find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, allSubobjectsOfType
from pontus.view import BasicView, ViewError, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI
from pontus.widget import CheckboxChoiceWidget, RichTextWidget
from pontus.schema import Schema
from pontus.form import FormView

from novaideo.content.processes.novaideo_view_manager.behaviors import  Search
from novaideo.content.novaideo_application import NovaIdeoApplicationSchema, NovaIdeoApplication
from novaideo import _
from novaideo.content.interface import Iidea, IProposal, IPerson


default_serchable_content = {'Idea': Iidea,
                             'Proposal': IProposal,
                             'Person': IPerson}


@colander.deferred
def content_types_choices(node, kw):
    values =[(k, k) for k in default_serchable_content.keys()]
    return CheckboxChoiceWidget(values=values, inline=True)


@colander.deferred
def default_content_types_choices(node, kw):
    return default_serchable_content.keys()


class SearchSchema(Schema):

    text = colander.SchemaNode(
        colander.String(),
        title=_(''),
        missing=''
        )
    content_types = colander.SchemaNode(
                colander.Set(),
                widget=content_types_choices, 
                title='',
                default=default_content_types_choices,
                missing=default_content_types_choices,
                )


@view_config(
    name='search',
    renderer='pontus:templates/view.pt',
    )
class SearchView(FormView):
    title = _('Search')
    name = 'search'
    coordinates = 'header'
    schema = SearchSchema()
    behaviors = [Search]
    formid = 'formsearch'
    item_template = 'pontus:templates/subview_sample.pt'

    def _get_appstruct(self):
        post = getattr(self, 'postedform', self.request.POST)
        form, reqts = self._build_form()
        form.formid = self.viewid + '_' + form.formid
        posted_formid = None
        if '__formid__' in post:
            posted_formid = post['__formid__']

        if posted_formid is not None and posted_formid == form.formid:
            try:
                post = post.copy()
                controls = post.items()
                validated = form.validate(controls)
                content_types = validated['content_types']
                if content_types:
                    return validated
                else:
                    validated['content_types'] = default_serchable_content.keys()
                    return validated
            except Exception as e:
                pass

        content_types = self.params('content_types')
        text = self.params('text')
        if text is None:
            text = ''

        if content_types is not None:
            content_types = content_types.split(',')
        else:
            content_types = default_serchable_content.keys()

        return {'content_types':content_types, 'text':text} 

    def before_update(self):
        root = getSite()
        #self.form_class.css_class = 'navbar-form navbar-left'
        self.action = self.request.resource_url(root, '')

    def default_data(self):
        appstruct = self._get_appstruct()
        
        return appstruct



@view_config(
    name='',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SearchResultView(BasicView):
    title = _('Nova-Ideo contents')
    name = ''
    validators = [Search.get_validator()]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'search_result'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/novaideo.js']}


    def update(self):
        formviewinstance = SearchView(self.context, self.request)
        formviewinstance.postedform = self.request.POST
        appstruct = formviewinstance._get_appstruct()
        content_types = appstruct['content_types']
        text = appstruct['text']
        if text == '':
            text = None

        if text is not None:
            text = [t.lower() for t in text.split(',')]
 
        root = getSite()
        interfaces = [default_serchable_content[i].__identifier__ for i in content_types]
        #catalog
        dace_catalog = find_catalog('dace')
        novaideo_catalog = find_catalog('novaideo')
        system_catalog = find_catalog('system')
        #index
        title_index = dace_catalog['object_title']
        description_index = dace_catalog['object_description']
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        containers_oids_index = dace_catalog['containers_oids']
        keywords_index = novaideo_catalog['object_keywords']
        text_index = system_catalog['text']
        name_index = system_catalog['name']
        #query
        query = None
        if text is not None:
            query = keywords_index.any(text) | \
                    name_index.any(text) | \
                    states_index.any(text)
            for t in text:
                query = query | \
                        title_index.contains(t) | \
                        description_index.contains(t) | \
                        text_index.contains(t)
            
        if query is None:
            query = object_provides_index.any(interfaces)
        else:
            query = (query) & object_provides_index.any(interfaces)

        resultset = query.execute()
        len_result = resultset.__len__()

        #if len_result > 2:
            #resultset = resultset.sort(title_index, raise_unsortable=False)

        objects = resultset.all()
        #TODO access control
        result_body = []
        for o in objects:
            object_values = {'object':o}
            body = self.content(result=object_values, template=o.result_template)['body']
            result_body.append(body)

        result = {}
        values = {
                'bodies': result_body,
                'length': len_result
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        result  = merge_dicts(self.requirements_copy, result)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({Search:SearchView})

