
import re
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.organization_management.behaviors import (
    SeeOrganizations)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='seeorganizations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SeeOrganizationsView(BasicView):
    title = _('Organizations')
    name = 'seeorganizations'
    behaviors = [SeeOrganizations]
    template = 'novaideo:views/organization_management/templates/see_organizations.pt'
    viewid = 'seeorganizations'


    def update(self):
        self.execute(None)
        result = {}

        all_organization_data = {'organizations':[]}
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                        'dace_ui_api')
        organizations_actions = dace_ui_api.get_actions(
                            self.context.organizations, self.request)
        action_updated, messages, \
        resources, actions = dace_ui_api.update_actions(self.request,
                                                        organizations_actions)
        for organization in self.context.organizations:
            organization_actions = [a for a in actions \
                                  if a['context'] is organization]

            logo = {}
            if getattr(organization, 'logo', None):
                logo = {'url':organization.logo.url(self.request), 
                        'title':organization.logo.title}

            description = organization.description
            reduced_description = description
            if len(description) > 249:
                description = description[:250]
                reduced_description = re.sub('\s[a-z0-9._-]+$', ' ...',
                                             description)

            organization_dic = { 
                'actions': organization_actions,
                'url':self.request.resource_url(organization, '@@index'), 
                'title': organization.title,
                'description': reduced_description,
                'logo': logo}
            all_organization_data['organizations'].append(organization_dic)
         
        all_organization_data['tabid'] = self.__class__.__name__ + \
                                         'OrganizationActions'
        body = self.content(result=all_organization_data, 
                            template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = action_updated
        result['coordinates'] = {self.coordinates:[item]}
        result.update(resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result

DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeOrganizations:SeeOrganizationsView})
