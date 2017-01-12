# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import math
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import Batch

from dace.util import get_obj, getSite
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView, ViewError

from novaideo.content.processes.smart_folder_management.behaviors import (
    SeeSmartFolder)
from novaideo.content.smart_folder import SmartFolder
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo import _, log
from novaideo.core import BATCH_DEFAULT_SIZE, can_access
from novaideo.utilities.smart_folder_utility import (
    get_folder_content, get_adapted_filter)
from novaideo.utilities.util import (
    generate_navbars,
    ObjectRemovedException,
    render_listing_obj,
    render_listing_objs)
from novaideo.views.filter import (
    merge_with_filter_view, get_filter, FILTER_SOURCES)
from novaideo.views.filter.sort import sort_view_objects


@view_config(
    name='seesmartfolder',
    context=SmartFolder,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeSmartFolderView(BasicView):
    title = ''
    name = 'seesmartfolder'
    behaviors = [SeeSmartFolder]
    template = 'novaideo:views/smart_folder_management/templates/see_smartfolder.pt'
    subfoldertemplate = 'novaideo:views/smart_folder_management/templates/see_smartfolders.pt'
    viewid = 'seesmartfolder'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        user = get_current()
        subfolders = [sf for sf in self.context.children
                      if can_access(user, sf)]
        subfolders = sorted(subfolders, key=lambda e: e.get_order())
        result_body, result = render_listing_objs(
            self.request, subfolders, user)
        values = {'object': self.context,
                  'subfolders': result_body,
                  'navbar_body': navbars['navbar_body'],
                  'body_actions': navbars['body_actions']
                  }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


@view_config(
    name='open',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class OpenFolderView(BasicView):
    title = _('Open the folder')
    name = 'open'
    breadcrumb_template = 'novaideo:views/templates/folder_breadcrumb.pt'
    templates = {'default': 'novaideo:views/novaideo_view_manager/templates/search_result.pt',
                 'bloc': 'novaideo:views/novaideo_view_manager/templates/search_result_blocs.pt'}
    viewid = 'open_folder'
    wrapper_template = 'novaideo:views/smart_folder_management/templates/folder_view_wrapper.pt'
    css_class = "open-folder simple-bloc"
    container_css_class = 'home'

    def _add_filter(self, folder, user):
        def source(**args):
            objects = get_folder_content(folder, user, sort_on=None, **args)
            return objects

        url = self.request.resource_url(
            self.context,
            '@@novaideoapi',
            query={'folderid': self.params('folderid')})
        fields = get_adapted_filter(folder, user)
        if not fields:
            return None, None

        return get_filter(
            self, url=url,
            source=source,
            **fields)

    def update(self):
        result = {}
        user = get_current()
        folderid = self.params('folderid')
        try:
            folder = get_obj(int(folderid))
        except:
            folder = None
        # if not valid folderid
        if folderid is None or folder is None:
            error = ViewError()
            error.principalmessage = _("Access to the requested folder has been denied")
            error.causes = [_("Folder not valid")]
            message = error.render_message(self.request)
            item = self.adapt_item('', self.viewid)
            item['messages'] = {error.type: [message]}
            result['coordinates'] = {self.coordinates: [item]}
            return result

        # if permission denied
        if folder and not can_access(user, folder):
            error = ViewError()
            error.principalmessage = _("Access to the requested folder has been denied")
            error.causes = [_("Permission denied")]
            message = error.render_message(self.request)
            item = self.adapt_item('', self.viewid)
            item['messages'] = {error.type: [message]}
            result['coordinates'] = {self.coordinates: [item]}
            return result

        # calling self._add_filter will set self.filter_instance or not
        template_type = getattr(folder, 'view_type', 'default')
        if template_type == 'bloc':
            self.wrapper_template = 'novaideo:views/smart_folder_management/templates/folder_blocs_view_wrapper.pt'

        filter_body = None
        filter_form, filter_data = self._add_filter(folder, user)
        args = merge_with_filter_view(self, {})
        objects = get_folder_content(folder, user, **args)
        objects, sort_body = sort_view_objects(
            self, objects,
            ['proposal', 'idea', 'amendment',
             'file', 'person'], user)
        len_result = len(objects)
        self.breadcrumb = self.content(
            args={'lineage': folder.folder_lineage,
                  'nember': len_result},
            template=self.breadcrumb_template)['body']
        self.title = '/'.join([f.title for f in folder.folder_lineage])
        if getattr(self, 'filter_instance', None) is not None:
            filter_data['filter_message'] = self.breadcrumb
            filter_body = getattr(self, 'filter_instance').get_body(filter_data)

        url = self.request.resource_url(
            self.context, 'open', query={'folderid': folderid})
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results"
        result_body = []

        for obj in batch:
            body = render_listing_obj(
                self.request, obj, user,
                view_type=template_type)
            if body:
                result_body.append(body)

        values = {
            'bodies': result_body,
            'batch': batch,
            'filter_body': filter_body,
            'sort_body': sort_body,
            'row_len': math.ceil(len_result/2)
            }
        template = self.templates.get(template_type, 'default')
        body = self.content(args=values, template=template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        if filter_form:
            result['css_links'] = filter_form['css_links']
            result['js_links'] = filter_form['js_links']

        return result

    def before_update(self):
        super(OpenFolderView, self).before_update()
        folderid = self.params('folderid')
        try:
            folder = get_obj(int(folderid))
            if folder:
                self.title = '/'.join([f.title for f in folder.folder_lineage])
        except (TypeError, ValueError):
            self.title = self.request.localizer.translate(_('Folder not valid'))
            user = get_current()
            log.info(
                "Folder not valid. id: ({folderid}) , user: ({user}, {email}) ".format(
                    user=getattr(user, 'title', getattr(user, 'name', 'Anonymous')),
                    email=getattr(user, 'email', 'Anonymous'),
                    folderid=folderid))


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeSmartFolder: SeeSmartFolderView})

FILTER_SOURCES.update({OpenFolderView.name: OpenFolderView})
