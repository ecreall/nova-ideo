
import re
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView, merge_dicts
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
        all_messages = {}
        isactive = False
        all_resources = {}
        all_resources['js_links'] = []
        all_resources['css_links'] = []
        all_organization_data = {'organizations':[]}
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                        'dace_ui_api')
        for organization in self.context.organizations:
            action_updated, messages, resources, actions = dace_ui_api._actions(self.request, organization)
            if action_updated and not isactive:
                isactive = True

            all_messages.update(messages)
            if resources is not None:
                if 'js_links' in resources:
                    all_resources['js_links'].extend(resources['js_links'])
                    all_resources['js_links'] = list(set(all_resources['js_links']))

                if 'css_links' in resources:
                    all_resources['css_links'].extend(resources['css_links'])
                    all_resources['css_links'] =list(set(all_resources['css_links']))

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
                'actions': actions,
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
        item['messages'] = all_messages
        item['isactive'] = isactive
        result['coordinates'] = {self.coordinates:[item]}
        result.update(all_resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result

DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeOrganizations:SeeOrganizationsView})
