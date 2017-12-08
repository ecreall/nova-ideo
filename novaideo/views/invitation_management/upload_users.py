# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel
from pontus.schema import Schema
from pontus.widget import FileWidget
from pontus.file import ObjectData, File

from novaideo.content.processes.invitation_management.behaviors import (
    UploadUsers)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


class UploadUsersStudyReport(BasicView):
    title = _('Alert for users import')
    name = 'alertforusersimport'
    template = 'novaideo:views/invitation_management/templates/alert_import.pt'

    def update(self):
        result = {}
        values = {}
        body = self.content(args={}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class UploadUsersSchema(Schema):

    file = colander.SchemaNode(
        ObjectData(File),
        widget=FileWidget(),
        title=_('The xls file'),
        description=_("The xls file containing invitations data.")
        )


class UploadUsersForm(FormView):

    title = _('Upload invitations')
    schema = UploadUsersSchema(editable=True)
    behaviors = [UploadUsers, Cancel]
    formid = 'formuploadusersform'
    name = 'upload_usersfrom'
    css_class = 'panel-transparent'



@view_config(
    name='upload_users',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class UploadUsersView(MultipleView):
    title = _('Upload invitations')
    name = 'upload_users'
    behaviors = [UploadUsers]
    viewid = 'upload_users'
    template = 'daceui:templates/mergedmultipleview.pt'
    css_class = 'panel-transparent'
    views = (UploadUsersStudyReport, UploadUsersForm)
    validators = [UploadUsers.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({UploadUsers:UploadUsersView})
