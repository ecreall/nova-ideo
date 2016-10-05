# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi, Sophie Jazwiecki

import colander
import json
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry
from pyramid.response import Response

from dace.processinstance.core import (
    Behavior, ValidationError, Validator)
from dace.objectofcollaboration.principal.util import (
    get_current, has_role)
from dace.util import find_catalog, getSite
from pontus.form import FormView
from pontus.schema import omit
from deform_treepy.widget import (
    DictSchemaType, KeywordsTreeWidget)

from novaideo import core
from novaideo.utilities.data_manager import (
    get_obj_value, get_attr_tree)
from novaideo import _
from . import WebServicesJsonView
from novaideo.views.filter import (
    find_entities, FilterSchema,
    MetadataFilter, metadata_filter_query,
    metadata_filter_analyzer,
    metadata_filter_data)
from novaideo.views.widget import (
    SimpleMappingtWidget)


def merge_dicts(dicts):
    result = {}
    for dict_ in dicts:
        result.update(dict_)

    return result


@view_config(name='webservices_finder')
class FindEntitiesJsonAPI(WebServicesJsonView):

    def find_entities(self):
        #page_limit, current_page, start, end = self._get_pagin_data()
        user = get_current()
        dace_catalog = find_catalog('dace')
        system_catalog = find_catalog('system')
        novaideo_catalog = find_catalog('novaideo')
        filter_schema = FindEntitiesJson(self.context, self.request)
        try:
            appstruct = filter_schema.calculate_posted_filter()
        except Exception as e:
            return {'items': [], 'total_count': 0, 'error': True,
                    'message': '{}: {}'.format(
                            e.__class__.__name__, e.args[0])}

        if appstruct is None:
            return {'items': [], 'total_count': 0, 'error': True,
                    'message': 'appstruct is None'}

        content_types_tree = appstruct['metadata_filter'].get('content_types', {}).copy()
        content_types = list(content_types_tree.keys())
        appstruct['metadata_filter'] = appstruct.get('metadata_filter', {})
        appstruct['metadata_filter']['content_types'] = content_types
        appstruct['dace'] = dace_catalog
        appstruct['system'] = system_catalog
        appstruct['novaideo'] = novaideo_catalog
        entities = find_entities(
            user=user, sort_on='release_date', include_site=True, **appstruct)

        def dumps(obj):
            """return values of attributes descibed in
               the colander schema node 'node' """
            registry = get_current_registry()
            content_type = registry.content.typeof(obj)
            fields = content_types_tree.get(content_type, {})
            result, to_add = get_obj_value(obj, fields)
            if result is None:
                return {}, to_add

            return result, to_add

        def merge_items(old_items, new_items):
            for item in new_items:
                oid = item.get('@id', None)
                if oid and oid not in old_items:
                    old_items[oid] = item
                elif oid:
                    old_item = old_items[oid]
                    old_items[oid] = merge_dicts([item, old_item])

        items = {}
        for entity in entities:
            values, to_add = dumps(entity)
            to_add.append(values)
            merge_items(items, to_add)

        result = {'items': list(items.values()), 'total_count': len(items)}
        response = Response()
        response.content_type = "application/json"
        response.text = json.dumps(result, indent=2)
        return response


class SendValidator(Validator):
    """The validor for the Send behavior"""

    @classmethod
    def validate(cls, context, request, **kw):
        if has_role(role=('SiteAdmin',)):
            return True

        raise ValidationError(msg=_("Permission denied"))


class Send(Behavior):

    behavior_id = "send"
    title = _("Send")
    description = ""

    @classmethod
    def get_validator(cls, **kw):
        return SendValidator

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@find"))


@colander.deferred
def keyword_widget(node, kw):
    tree = {}
    for name, content_type in core.SEARCHABLE_CONTENTS.items():
        tree.update({name: get_attr_tree(content_type=content_type)})

    tree = json.dumps(tree)
    return KeywordsTreeWidget(
        source_tree=tree,)


class FindMetadataFilter(MetadataFilter):

    content_types = colander.SchemaNode(
        typ=DictSchemaType(),
        widget=keyword_widget,
        default={},
        missing={},
        title=_('Content type'),
        )


class FindFilterSchema(FilterSchema):

    metadata_filter = omit(FindMetadataFilter(
        widget=SimpleMappingtWidget(
            mapping_css_class='controled-form',
            ajax=True,
            activator_icon="glyphicon glyphicon-cog",
            activator_title=_('Metadata filter')),
        query=metadata_filter_query,
        analyzer=metadata_filter_analyzer,
        filter_analyzer=metadata_filter_data
        ),
            ["_csrf_token_"])


@view_config(name='find',
             renderer='novaideo:web_services/templates/grid.pt',
             layout='web_services_layout')
class FindEntitiesJson(FormView):

    """Find entities form."""

    title = _('Find entities')
    name = 'find'
    schema = FindFilterSchema()
    behaviors = [Send]

    def calculate_posted_filter(self):
        form, reqts = self._build_form()
        form.formid = self.viewid + '_' + form.formid
        posted_formid = None
        if '__formid__' in self.request.POST:
            posted_formid = self.request.POST['__formid__']

        if posted_formid is not None and posted_formid == form.formid:
            controls = self.request.POST.items()
            validated = form.validate(controls)
            return validated

        return None

    def before_update(self):
        root = getSite()
        self.action = self.request.resource_url(
            root, '@@webservices_finder',
            query={'op': 'find_entities'})
