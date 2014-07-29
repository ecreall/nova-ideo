import re
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView, ViewError, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.invitation_management.behaviors import  SeeInvitations
from novaideo.content.novaideo_application import NovaIdeoApplicationSchema, NovaIdeoApplication



@view_config(
    name='seeinvitations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SeeInvitationsView(BasicView):
    title = 'Invitations'
    name = 'seeinvitations'
    behaviors = [SeeInvitations]
    template = 'novaideo:views/invitation_management/templates/see_invitations.pt'
    viewid = 'seeinvitations'


    def _modal_views(self, all_actions, form_id):
        action_updated=False
        resources = {}
        resources['js_links'] = []
        resources['css_links'] = []
        allbodies_actions = []
        updated_view = None
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        for t in all_actions:
            a = t[1]
            c = t[0]
            view = DEFAULTMAPPING_ACTIONS_VIEWS[a.action._class_]
            view_instance = view(c, self.request, behaviors=[a.action])
            view_result = {}
            if not action_updated and form_id is not None and form_id.startswith(view_instance.viewid):
                action_updated = True
                updated_view = view_instance
                view_result = view_instance()
            else:
                view_result = view_instance.get_view_requirements()

            if updated_view is view_instance and  view_instance.isexecutable and view_instance.finished_successfully:
                return True, True, None, None

            if isinstance(view_result, dict):
                action_infos = {}
                if updated_view is view_instance and (not view_instance.isexecutable or (view_instance.isexecutable and not view_instance.finished_successfully)) :
                    action_infos['toreplay'] = True
                    if not view_instance.isexecutable:
                        action_infos['finished'] = True

                body = ''
                if 'coordinates' in view_result:
                    body = view_instance.render_item(view_result['coordinates'][view_instance.coordinates][0], view_instance.coordinates, None)


                action_infos.update(dace_ui_api.action_infomrations(action=a.action, context=c, request=self.request))
                action_infos.update({'body':body,
                             'actionurl': a.url,
                             'data': c})
                allbodies_actions.append(action_infos)
                if 'js_links' in view_result:
                    resources['js_links'].extend(view_result['js_links'])
                    resources['js_links'] = list(set(resources['js_links']))

                if 'css_links' in view_result:
                    resources['css_links'].extend(view_result['css_links'])
                    resources['css_links'] =list(set(resources['css_links']))

                if 'finished' in action_infos:
                    view_resources= {}
                    view_resources['js_links'] = []
                    view_resources['css_links'] = []
                    if 'js_links' in view_result:
                        view_resources['js_links'].extend(view_result['js_links'])

                    if 'css_links' in view_result:
                        view_resources['css_links'].extend(view_result['css_links'])

                    return True, True, view_resources, [action_infos]


        return False, action_updated, resources, allbodies_actions

    def _actions(self, object):
        all_actions = []
        messages = {}
        actions = [a for a in object.actions]
        actions = sorted(actions, key=lambda a: a.action.__name__)
        p_actions = [(object,a) for a in actions]
        all_actions.extend(p_actions)
        from substanced.util import get_oid
        object_oid = str(get_oid(object))
        form_id = None
        if '__formid__' in self.request.POST:
            if self.request.POST['__formid__'].find(object_oid)>=0:
                form_id = self.request.POST['__formid__']

        toreplay, action_updated, resources, allbodies_actions = self._modal_views(all_actions, form_id)
        if toreplay:
            self.request.POST.clear()
            old_resources = resources
            old_allbodies_actions = allbodies_actions
            action_updated, messages, resources, allbodies_actions = self._actions(object)
            if old_resources is not None:
                if 'js_links' in old_resources:
                    resources['js_links'].extend(old_resources['js_links'])
                    resources['js_links'] = list(set(resources['js_links']))

                if 'css_links' in old_resources:
                    resources['css_links'].extend(old_resources['css_links'])
                    resources['css_links'] =list(set(resources['css_links']))

            if old_allbodies_actions is not None:
                allbodies_actions.extend(old_allbodies_actions)

            return True , messages, resources, allbodies_actions

        if form_id is not None and not action_updated:
            error = ViewError()
            error.principalmessage = u"Action non realisee"
            error.causes = ["Vous n'avez plus le droit de realiser cette action.", "L'action est verrouillee par un autre utilisateur."]
            message = self._get_message(error)
            messages.update({error.type: [message]})

        return action_updated, messages, resources, allbodies_actions

    def update(self):
        self.execute(None)
        result = {}
        all_messages = {}
        isactive = False
        all_resources = {}
        all_resources['js_links'] = []
        all_resources['css_links'] = []
        all_invitation_data = {'invitations':[]}
        for invitation in self.context.invitations:
            action_updated, messages, resources, actions = self._actions(invitation)
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

            state = None
            if invitation.state:
                state = invitation.state[0]

            invitation_dic = { 
                'actions': actions,
                'url':self.request.resource_url(invitation, '@@index'), 
                'first_name': getattr(invitation, 'first_name',''),
                'last_name': getattr(invitation, 'last_name', ''),
                'user_title': getattr(invitation, 'user_title', ''),
                'roles':getattr(invitation, 'roles', ''),
                'organization':getattr(invitation, 'organization', None),
                'state':state}
            all_invitation_data['invitations'].append(invitation_dic)
         
        all_invitation_data['tabid'] = self.__class__.__name__+'InvitationActions'
        body = self.content(result=all_invitation_data, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = all_messages
        item['isactive'] = isactive
        result['coordinates'] = {self.coordinates:[item]}
        result.update(all_resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result



DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitations:SeeInvitationsView})
