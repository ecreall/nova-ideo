# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.default_behavior import Cancel
from pontus.schema import select
from pontus.file import OBJECT_OID

from novaideo.content.processes.\
    newsletter_management.behaviors import (
        ConfigureNewsletter)
from novaideo.content.newsletter import (
    NewsletterSchema, Newsletter)
from novaideo import _
from novaideo.utilities.util import add_file_data


@view_config(
    name='configurenewsletter',
    context=Newsletter,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfigureNewsletterView(FormView):

    title = _('Configure the newsletter')
    schema = select(NewsletterSchema(editable=True),
                    ['working_params_conf', 'rec_conf'])
    behaviors = [ConfigureNewsletter, Cancel]
    formid = 'formeconfigurenewsletter'
    name = 'configurenewsletter'

    def default_data(self):
        data = self.context.get_data(self.schema)
        work_param = data.get('working_params_conf', {})
        if work_param:
            work_param = add_file_data(work_param, 'content_template')
            data['working_params_conf'] = work_param

        data[OBJECT_OID] = str(get_oid(self.context))
        return data


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ConfigureNewsletter: ConfigureNewsletterView})
