# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.organization_management.behaviors import (
    SeeOrganization)
from novaideo.content.organization import Organization
from novaideo import _


@view_config(
    name='seeorganization',
    context=Organization,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeOrganizationView(BasicView):
    title = _('Details')
    name = 'seeorganization'
    behaviors = [SeeOrganization]
    template = 'novaideo:views/organization_management/templates/see_organization.pt'
    viewid = 'seeorganization'


    def update(self):
        self.execute(None)
        result = {}
        logo = {}
        if getattr(self.context, 'logo', None):
            logo = {'url':self.context.logo.url(self.request), 
                    'title':self.context.logo.title}

        values = {
                'title': self.context.title,
                'description': self.context.description,
                'email':getattr(self.context, 'email', ''),
                'phone':getattr(self.context, 'phone', ''),
                'fax': getattr(self.context, 'fax', ''),
                'logo': logo,
                'members' : [m.name for m in self.context.members],
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeOrganization:SeeOrganizationView})