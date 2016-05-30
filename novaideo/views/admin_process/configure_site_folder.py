# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.file import OBJECT_OID

from novaideo.content.processes.admin_process.behaviors import (
    ConfigureSite)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication, NovaIdeoApplicationSchema)
from novaideo import _
from novaideo.mail import DEFAULT_SITE_MAILS


def add_file_data(container, attr):
    file_ = container.get(attr, None)
    if file_ and hasattr(file_, 'get_data'):
        container[attr] = file_.get_data(None)
        container[attr][OBJECT_OID] = str(get_oid(file_))

    return container


@view_config(
    name='configuresite',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfigureSiteView(FormView):

    title = _('Configure the site')
    schema = select(NovaIdeoApplicationSchema(
                        factory=NovaIdeoApplication,
                        editable=True),
                        # omit=('work_conf',)),
                    ['work_conf',
                     'user_conf',
                     'notif_conf',
                     'keywords_conf',
                     'mail_conf',
                     'ui_conf',
                     'other_conf'
                     ])
    behaviors = [ConfigureSite, Cancel]
    formid = 'formconfiguresite'
    name = 'configuresite'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/contact_management.js']}

    def default_data(self):
        localizer = self.request.localizer
        data = self.context.get_data(self.schema)
        templates = [self.context.get_mail_template(mail_id)
                     for mail_id in DEFAULT_SITE_MAILS]
        for template in templates:
            template['title'] = localizer.translate(
                template['title'])

        ui_conf = data.get('ui_conf', {})
        if ui_conf:
            ui_conf = add_file_data(ui_conf, 'picture')
            ui_conf = add_file_data(ui_conf, 'favicon')
            ui_conf = add_file_data(ui_conf, 'theme')
            data['ui_conf'] = ui_conf

        templates = sorted(templates, key=lambda e: e['mail_id'])
        data['mail_conf'] = {'mail_templates': templates}
        data[OBJECT_OID] = str(get_oid(self.context))
        # deadlines = getattr(self.context, 'deadlines', [])
        # if deadlines:
        #     data['work_conf']['deadline'] = deadlines[-1]

        return data


DEFAULTMAPPING_ACTIONS_VIEWS.update({ConfigureSite: ConfigureSiteView})
