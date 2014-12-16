# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.activity import ActionType
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.organization_management.behaviors import (
    SeeOrganization)
from novaideo.content.organization import Organization


@view_config(
    name='',
    context=Organization,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeOrganizationView(BasicView):
    title = ''
    name = 'seeorganization'
    behaviors = [SeeOrganization]
    template = 'novaideo:views/organization_management/templates/see_organization.pt'
    viewid = 'seeorganization'


    def update(self):
        self.execute(None)
        result = {}
        actions = [a for a in self.context.actions \
                   if a.action.actionType != ActionType.automatic]
        values = {'object': self.context,
                  'actions': actions}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeOrganization:SeeOrganizationView})