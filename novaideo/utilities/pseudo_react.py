# -*- coding: utf8 -*-
# Copyright (c) 2016 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import json
from pyramid.threadlocal import get_current_registry
from pyramid import renderers
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import find_resource

from daceui.interfaces import IDaceUIAPI
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import (
    get_current)
from dace.util import getAllBusinessAction

from novaideo import _, nothing
from novaideo.views.idea_management.comment_idea import (
    CommentsView)
from novaideo.views.user_management.discuss import (
    DiscussCommentsView,
    GeneralCommentsView)
from novaideo.views.idea_management.present_idea import (
    SentToView)
from novaideo.views.novaideo_view_manager.see_my_supports import (
    CONTENTS_MESSAGES)
from novaideo.views.novaideo_view_manager.see_my_selections import (
    CONTENTS_MESSAGES as SELECT_CONTENTS_MESSAGES)
from novaideo.views.user_management.see_registrations import (
    CONTENTS_MESSAGES as REGISTRATION_CONTENTS_MESSAGES)
from novaideo.views.invitation_management.see_invitations import (
    CONTENTS_MESSAGES as INVITATION_CONTENTS_MESSAGES)
from novaideo.views.organization_management.see_organizations import (
    CONTENTS_MESSAGES as ORGANIZATION_CONTENTS_MESSAGES)
from novaideo.utilities.util import (
    update_all_ajax_action, render_listing_obj)
from novaideo.views.filter import find_entities
from novaideo.content.interface import (
    IPreregistration, IInvitation, IOrganization)
from novaideo.content.organization import Organization
from novaideo.content.person import Person


def get_navbar_updated_data(view, **kwargs):
    result = {}
    action_id = kwargs.get('action_id', None)
    if action_id:
        localizer = view.request.localizer
        result['action_id'] = action_id
        result['components'] = [kwargs.get('navbr_action_id')]
        result['navbar_item_nb'] = kwargs.get('navbar_item_nb', 0)
        result['navbar_all_item_nb'] = kwargs.get('navbar_all_item_nb', None)
        result['navbar_title'] = localizer.translate(kwargs.get('navbar_title'))
        result['view_url'] = kwargs.get('view_url')
        result['view_title'] = kwargs.get('view_title')
        result['navbar_icon'] = kwargs.get('navbar_icon')
        result['view_name'] = kwargs.get('view_name')
        result['removed'] = kwargs.get('removed')
        result['force_remove'] = kwargs.get('force_remove', False)
        result['alert_msg'] = kwargs.get('alert_msg', None)
        result['alert_type'] = kwargs.get('alert_type', None)

    return result


def get_footer_action_updated_data(view, **kwargs):
    result = {}
    action_id = kwargs.get('action_id', None)
    if action_id:
        localizer = view.request.localizer
        result['action_id'] = action_id
        result['components'] = [kwargs.get('footer_action_id')]
        result['action_item_nb'] = kwargs.get('action_item_nb')
        result['action_title'] = localizer.translate(kwargs.get('action_title'))
        result['action_icon'] = kwargs.get('action_icon')
        result['action_view_title'] = localizer.translate(
            kwargs.get('action_view_title', result['action_title']))
        result['has_opposit'] = kwargs.get('has_opposit', False)
        result['new_component_id'] = kwargs.get('new_component_id', None)
        result['opposit_action_id'] = kwargs.get('opposit_action_id', None)
        result['opposit_actionurl_update'] = kwargs.get(
            'opposit_actionurl_update', None)
        result['opposit_actionurl_after'] = kwargs.get(
            'opposit_actionurl_after', None)
        result['alert_msg'] = kwargs.get('alert_msg', None)
        result['alert_type'] = kwargs.get('alert_type', None)

    return result


def get_dropdown_action_updated_data(view, **kwargs):
    result = {}
    action_id = kwargs.get('action_id', None)
    if action_id:
        localizer = view.request.localizer
        result['action_id'] = action_id
        result['components'] = [kwargs.get('dropdown_action_id')]
        result['action_title'] = localizer.translate(kwargs.get('action_title'))
        result['action_icon'] = kwargs.get('action_icon')
        result['new_components'] = [kwargs.get('new_channel')]
        result['action_view_title'] = localizer.translate(
            kwargs.get('action_view_title', result['action_title']))
        result['has_opposit'] = kwargs.get('has_opposit', False)
        result['new_component_id'] = kwargs.get('new_component_id', None)
        result['opposit_action_id'] = kwargs.get('opposit_action_id', None)
        result['opposit_actionurl_update'] = kwargs.get(
            'opposit_actionurl_update', None)
        result['opposit_actionurl_after'] = kwargs.get(
            'opposit_actionurl_after', None)
        result['alert_msg'] = kwargs.get('alert_msg', None)
        result['alert_type'] = kwargs.get('alert_type', None)

    return result


def get_redirect_updated_data(view, **kwargs):
    result = {}
    action_id = kwargs.get('action_id', None)
    if action_id:
        result['action_id'] = action_id
        result['redirect_url'] = kwargs.get('redirect_url', None)
        result['new_body'] = kwargs.get('new_body')
        result['view_title'] = kwargs.get('view_title', None)
        result['view_name'] = kwargs.get('view_name', None)
        result['new_obj_body'] = kwargs.get('new_obj_body', None)
        result['removed'] = kwargs.get('removed', False)
        result['force_remove'] = kwargs.get('force_remove', False)
        result['alert_msg'] = kwargs.get('alert_msg', None)
        result['alert_type'] = kwargs.get('alert_type', None)

    return result


DATA_GETTERS = {
    'support_action': [get_navbar_updated_data],
    'footer_action': [
        get_footer_action_updated_data,
        get_navbar_updated_data,
        get_redirect_updated_data],
    'redirect_action': [get_redirect_updated_data],
    'dropdown_action': [get_dropdown_action_updated_data]
}


def get_components_data(action, view, **kwargs):
    getters = DATA_GETTERS.get(action, [])
    kwargs['action_id'] = action
    result = {'components': []}
    for getter in getters:
        res = getter(view, **kwargs)
        result['components'].extend(res.pop('components', []))
        result.update(res)

    return result


def get_default_action_metadata(action, request, context, api, **kwargs):
    redirect_url = None
    body = None
    if 'view_data' in kwargs:
        view_instance, view_result = kwargs['view_data']
        if view_result and view_result is not nothing:
            if isinstance(view_result, HTTPFound):
                redirect_url = view_result.headers['location']
            else:
                body = view_result['coordinates'][view_instance.coordinates][0]['body']

    result = {
        'action': 'redirect_action',
        'view': api,
        'redirect_url': redirect_url,
        'new_body': json.dumps(body) if body else None
    }
    return result


def get_edit_entity_metadata(
    action, request, context, api,
    msg=None, view_name=None, **kwargs):
    is_listing = api.params('is_listing')
    source_path = api.params('source_path')
    is_listing = json.loads(is_listing) if is_listing else False
    alert_msg = None
    new_obj_body = None
    redirect_url = None
    is_excuted = False
    body = None
    if 'view_data' in kwargs:
        view_instance, view_result = kwargs['view_data']
        if view_result and view_result is not nothing:
            if isinstance(view_result, HTTPFound):
                is_excuted = True
                alert_msg = msg
                if is_listing:
                    if request.POST:
                        request.POST.clear()

                    request.invalidate_cache = True
                    new_obj_body = render_listing_obj(
                        request, context, get_current())
                else:
                    redirect_url = view_result.headers['location']
            else:
                body = view_result['coordinates'][view_instance.coordinates][0]['body']

    result = {
        'action': 'redirect_action',
        'view': api,
        'redirect_url': redirect_url,
        'view_name': view_name,
        'new_obj_body': new_obj_body,
        'new_body': json.dumps(body) if body else None
    }
    result['alert_msg'] = request.localizer.translate(alert_msg) if alert_msg else None
    result['alert_type'] = 'success'
    result['is_listing'] = is_listing
    result['source_path'] = source_path
    result['is_excuted'] = is_excuted
    return result


def get_dirct_edit_entity_metadata(
    action, request, context, api,
    msg=None, view_name=None, **kwargs):
    is_listing = api.params('is_listing')
    is_listing = json.loads(is_listing) if is_listing else False
    alert_msg = None
    new_obj_body = None
    redirect_url = None
    alert_msg = msg
    if is_listing:
        if request.POST:
            request.POST.clear()

        request.invalidate_cache = True
        new_obj_body = render_listing_obj(
            request, context, get_current())
    else:
        redirect_url = request.resource_url(context, '@@index')

    result = {
        'action': 'redirect_action',
        'view': api,
        'redirect_url': redirect_url,
        'view_name': view_name,
        'new_obj_body': new_obj_body
    }
    result['alert_msg'] = request.localizer.translate(alert_msg) if alert_msg else None
    result['alert_type'] = 'success'
    return result


def get_subscribtion_metadata(action, request, context, api, **kwargs):
    alert_msg = _("Vous n'êtes plus abonné à la discussion.")
    opposit_action = 'subscribe'
    if action.node_id == 'subscribe':
        alert_msg = _('Vous êtes maintenant abonné à la discussion.')
        opposit_action = 'unsubscribe'

    opposit_actions = getAllBusinessAction(
        context, request, node_id=opposit_action,
        process_discriminator='Application')
    result = {
        'action': 'dropdown_action',
        'view': api,
    }
    subject = context.subject
    user = get_current()
    new_channel = ''
    if subject:
        actions_call, action_resources = update_all_ajax_action(
            subject, request, 'comment')
        if actions_call:
            object_values = {
                'object': context,
                'current_user': user,
                'action_call': actions_call[0]}
            new_channel = renderers.render(
                context.templates.get('default'),
                object_values,
                request)

    if opposit_actions:
        opposit_action = opposit_actions[0]
        dace_ui_api = get_current_registry().getUtility(
            IDaceUIAPI, 'dace_ui_api')
        opposit_action_inf = dace_ui_api.action_infomrations(
            opposit_action, context, request)
        actionoid = str(getattr(action, '__oid__', 'entityoid'))
        oppositactionoid = str(getattr(
            opposit_action, '__oid__', 'entityoid'))
        contextoid = str(getattr(
            context, '__oid__', 'entityoid'))
        action_view = DEFAULTMAPPING_ACTIONS_VIEWS[opposit_action.__class__]
        action_view_title = action_view.title

        result.update({
            'dropdown_action_id': actionoid + '-' + contextoid,
            'action_title': opposit_action.title,
            'action_icon': getattr(opposit_action, 'style_picto', ''),
            'action_view_title': action_view_title,
            'new_channel': new_channel,
            'has_opposit': True,
            'new_component_id': oppositactionoid + '-' + contextoid,
            'opposit_action_id': opposit_action_inf.get('action_id'),
            'opposit_actionurl_update': opposit_action_inf.get(
                'actionurl_update'),
            'opposit_actionurl_after': opposit_action_inf.get('after_url'),
            'alert_msg': request.localizer.translate(alert_msg),
            'alert_type': 'success'
        })

    return result


def get_selection_metadata(action, request, context, api, **kwargs):
    opposit_action = 'select'
    alert_msg = _('${context} ne fait maintenant plus partie de vos suivis.',
                  mapping={'context': context.title})
    removed = True
    if action.node_id == 'select':
        removed = False
        opposit_action = 'deselect'
        alert_msg = _('${context} fait maintenant partie de vos suivis.',
                      mapping={'context': context.title})

    opposit_actions = getAllBusinessAction(
        context, request, node_id=opposit_action,
        process_discriminator='Application')
    result = {
        'action': 'footer_action',
        'view': api,
    }
    if opposit_actions:
        user = get_current()
        localizer = request.localizer
        opposit_action = opposit_actions[0]
        dace_ui_api = get_current_registry().getUtility(
            IDaceUIAPI, 'dace_ui_api')
        opposit_action_inf = dace_ui_api.action_infomrations(
            opposit_action, context, request)
        actionoid = str(getattr(action, '__oid__', 'entityoid'))
        oppositactionoid = str(getattr(
            opposit_action, '__oid__', 'entityoid'))
        contextoid = str(getattr(
            context, '__oid__', 'entityoid'))
        len_selection = getattr(context, 'len_selections', 0)
        len_all_selection = len(getattr(user, 'selections', 0))
        index = str(len_all_selection)
        if len_all_selection > 1:
            index = '*'

        view_title = localizer.translate(
            _(SELECT_CONTENTS_MESSAGES[index],
              mapping={'nember': len_all_selection}))
        action_view = DEFAULTMAPPING_ACTIONS_VIEWS[opposit_action.__class__]
        action_view_title = action_view.title
        result.update({
            'footer_action_id': actionoid + '-' + contextoid,
            'navbr_action_id': 'myselections',
            'action_item_nb': len_selection,
            'navbar_item_nb': len_all_selection,
            'action_title': opposit_action.title,
            'navbar_title': _('My following'),
            'action_view_title': action_view_title,
            'view_title': view_title,
            'action_icon': getattr(opposit_action, 'style_picto', ''),
            'navbar_icon': 'glyphicon glyphicon-star-empty',
            'view_url': request.resource_url(
                request.root, 'seemyselections'),
            'view_name': 'seemyselections',
            'removed': removed,
            'has_opposit': True,
            'new_component_id': oppositactionoid + '-' + contextoid,
            'opposit_action_id': opposit_action_inf.get('action_id'),
            'opposit_actionurl_update': opposit_action_inf.get(
                'actionurl_update'),
            'opposit_actionurl_after': opposit_action_inf.get('after_url'),
            'alert_msg': localizer.translate(alert_msg),
            'alert_type': 'success'
        })

    return result


def get_support_metadata(action, request, context, api, **kwargs):
    node_id = action.node_id
    alert_msg = None
    if node_id == 'oppose':
        alert_msg = _('Vous êtes maintenant opposé au contenu ${context}.',
                      mapping={'context': context.title})
    elif node_id == 'support':
        alert_msg = _('Vous soutenez maintenant le contenu ${context}.',
                      mapping={'context': context.title})
    elif node_id == 'withdraw_token':
        alert_msg = _('Votre jeton est bien récupéré du contenu ${context}.',
                      mapping={'context': context.title})

    user = get_current()
    localizer = request.localizer
    item_nb = len(getattr(user, 'supports', []))
    len_tokens = len(getattr(user, 'tokens', []))
    index = str(item_nb)
    if item_nb > 1:
        index = '*'

    result = {
        'action': 'support_action',
        'view': api,
        'navbar_item_nb': item_nb,
        'navbar_all_item_nb': len(getattr(user, 'tokens_ref', [])),
        'navbr_action_id': 'mysupports',
        'navbar_title': localizer.translate(_("My supports")),
        'view_url': request.resource_url(
            request.root, 'seemysupports'),
        'view_title': localizer.translate(
            _(CONTENTS_MESSAGES[index],
              mapping={'nember': item_nb,
                       'tokens': len_tokens})),
        'navbar_icon': "ion-ios7-circle-filled",
        'view_name': 'seemysupports',
        'removed': action.node_id == 'withdraw_token',
        'alert_msg': localizer.translate(alert_msg),
        'alert_type': 'success'
    }
    return result


#Chanels

def get_comment_metadata(action, request, context, api, **kwargs):
    body = None
    if 'view_data' in kwargs:
        comments = [context.channel.comments[-1]]
        result_view = CommentsView(context, request)
        result_view.comments = comments
        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

    actionoid = str(getattr(action, '__oid__', 'entityoid'))
    contextoid = str(getattr(
        context, '__oid__', 'entityoid'))
    result = {
        'action': 'footer_action',
        'view': api,
        'footer_action_id': actionoid + '-' + contextoid,
        'action_item_nb': context.channel.len_comments,
        'action_title': action.title,
        'action_icon': getattr(action, 'style_picto', ''),
        'new_body': body
    }
    return result


def get_edit_comment_metadata(action, request, context, api, **kwargs):
    body = None
    if 'view_data' in kwargs:
        comments = [context]
        result_view = CommentsView(context, request)
        result_view.comments = comments
        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

    result = {
        'action': 'footer_action',
        'view': api,
        'new_body': body}
    return result


def get_remove_comment_metadata(action, request, context, api, **kwargs):
    result = {
        'action': 'footer_action',
        'view': api}
    channel = kwargs.get('channel')
    if context:
        comment_actions = getAllBusinessAction(
            context, request, node_id='comment',
            process_discriminator='Application')
        comment_actions.extend(getAllBusinessAction(
            context, request, node_id='discuss',
            process_discriminator='Application'))
        if comment_actions:
            action = comment_actions[0]
            actionoid = str(getattr(action, '__oid__', 'entityoid'))
            contextoid = str(getattr(
                context, '__oid__', 'entityoid'))
            result.update({
                'footer_action_id': actionoid + '-' + contextoid,
                'action_item_nb': channel.len_comments,
                'action_title': action.title,
                'action_icon': getattr(action, 'style_picto', ''),
                'alert_msg': request.localizer.translate(_('Le commentaire est maintenant supprimé.')),
                'alert_type': 'success'
            })

    return result


def get_general_discuss_metadata(action, request, context, api, **kwargs):
    body = None
    if 'view_data' in kwargs:
        channel = context.channel
        comments = [channel.comments[-1]]
        result_view = GeneralCommentsView(context, request)
        result_view.comments = comments
        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

    result = {
        'action': 'footer_action',
        'view': api,
        'new_body': body}
    return result


def get_discuss_metadata(action, request, context, api, **kwargs):
    body = None
    if 'view_data' in kwargs:
        user = get_current()
        channel = context.get_channel(user)
        comments = [channel.comments[-1]]
        result_view = DiscussCommentsView(context, request)
        result_view.comments = comments
        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

    actionoid = str(getattr(action, '__oid__', 'entityoid'))
    contextoid = str(getattr(
        context, '__oid__', 'entityoid'))
    channel = kwargs.get('channel', None)
    result = {
        'action': 'footer_action',
        'view': api,
        'footer_action_id': actionoid + '-' + contextoid,
        'action_item_nb': getattr(channel, 'len_comments', 0),
        'action_title': action.title,
        'action_icon': getattr(action, 'style_picto', ''),
        'new_body': body
    }
    return result


def get_respond_metadata(action, request, context, api, **kwargs):
    body = None
    if 'view_data' in kwargs:
        request.POST.clear()
        comments = [context.comments[-1]]
        result_view = CommentsView(context, request)
        result_view.comments = comments
        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

    channel = context.channel
    subject = channel.subject
    result = {
        'action': 'footer_action',
        'view': api,
        'new_body': body}
    if subject:
        comment_actions = getAllBusinessAction(
            subject, request, node_id='comment',
            process_discriminator='Application')
        comment_actions.extend(getAllBusinessAction(
            subject, request, node_id='discuss',
            process_discriminator='Application'))
        if comment_actions:
            action = comment_actions[0]
            actionoid = str(getattr(action, '__oid__', 'entityoid'))
            contextoid = str(getattr(
                subject, '__oid__', 'entityoid'))
            result.update({
                'footer_action_id': actionoid + '-' + contextoid,
                'action_item_nb': channel.len_comments,
                'action_title': action.title,
                'action_icon': getattr(action, 'style_picto', '')
            })

    return result



def get_present_metadata(action, request, context, api, **kwargs):
    body = None
    if 'view_data' in kwargs:
        result_view = SentToView(context, request)
        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

    actionoid = str(getattr(action, '__oid__', 'entityoid'))
    contextoid = str(getattr(
        context, '__oid__', 'entityoid'))
    result = {
        'action': 'footer_action',
        'view': api,
        'footer_action_id': actionoid + '-' + contextoid,
        'action_item_nb': context.len_contacted,
        'action_title': action.title,
        'action_icon': getattr(action, 'style_picto', ''),
        'new_body': body
    }
    return result


def get_withdraw_user_metadata(action, request, context, api, **kwargs):
    source_path = api.params('source_path')
    source_context = None
    removed = False
    new_obj_body = None
    redirect_url = None
    alert_msg = None
    executed = False
    if source_path:
        source_path = '/'.join(source_path.split('/')[:-1])
        source_context = find_resource(request.root, source_path)
        if source_context:
            if isinstance(source_context, Organization):
                removed = True
                executed = True
            elif not isinstance(source_context, Person):
                if request.POST:
                    request.POST.clear()

                request.invalidate_cache = True
                new_obj_body = render_listing_obj(
                    request, context, get_current())
                executed = True
            elif 'view_data' in kwargs:
                view_instance, view_result = kwargs['view_data']
                if view_result and view_result is not nothing:
                    if isinstance(view_result, HTTPFound):
                        redirect_url = view_result.headers['location']
                        executed = True

    if executed:
        alert_msg = _("Le membre ${context} est bien retiré de l'organisation.",
                      mapping={'context': context.title})
    result = {
        'action': 'redirect_action',
        'view': api,
        'redirect_url': redirect_url,
        'removed': removed,
        'view_name': 'index',
        'new_obj_body': new_obj_body,
        'new_body': None,
        'alert_msg': request.localizer.translate(alert_msg) if alert_msg else None,
        'alert_type': 'success'
    }
    return result


#Invitations

def get_remove_invitation_metadata(action, request, context, api, **kwargs):
    removed = False
    redirect_url = None
    view_name = 'seeinvitations'
    is_listing = api.params('is_listing')
    is_listing = json.loads(is_listing) if is_listing else False
    if is_listing:
        removed = True
    else:
        redirect_url = request.resource_url(request.root, '@@'+view_name)

    user = get_current()
    objects = find_entities(
        user=user,
        interfaces=[IInvitation])
    len_result = len(objects)
    index = str(len_result)
    if len_result > 1:
        index = '*'

    view_title = request.localizer.translate(
        _(INVITATION_CONTENTS_MESSAGES[index],
          mapping={'nember': len_result}))
    result = {
        'action': 'redirect_action',
        'view': api,
        'redirect_url': redirect_url,
        'view_title': view_title,
        'removed': removed,
        'view_name': view_name,
    }
    result['alert_msg'] = request.localizer.translate(
        _("L'invitation a bien été supprimée."))
    result['alert_type'] = 'success'
    return result


def get_edit_invitation_metadata(action, request, context, api, **kwargs):
    result = get_edit_entity_metadata(
        action, request, context, api,
        _("L'invitation a bien été modifiée."),
        'seeinvitations', **kwargs)
    return result


def get_remind_invitation_metadata(action, request, context, api, **kwargs):
    return get_dirct_edit_entity_metadata(
        action, request, context, api,
         _("L'invité ${context} a bien été rappelé.",
          mapping={'context': context.first_name + ' ' + context.last_name}),
        'seeinvitations', **kwargs)


#Registrations

def get_remind_registration_metadata(action, request, context, api, **kwargs):
    return get_edit_entity_metadata(
        action, request, context, api,
        _("L'inscrit ${context} a bien été rappelé.",
        mapping={'context': context.first_name + ' ' + context.last_name}),
        'seeregistrations', **kwargs)


def get_accept_registration_metadata(action, request, context, api, **kwargs):
    return get_edit_entity_metadata(
        action, request, context, api,
        _("L'inscription de ${context} a bien été accepter.",
          mapping={'context': context.first_name + ' ' + context.last_name}),
        'seeregistrations', **kwargs)


def get_remove_registration_metadata(action, request, context, api, **kwargs):
    result = get_edit_entity_metadata(
        action, request, context, api,
        _("L'inscription a bien été supprimée."),
        'seeregistrations', **kwargs)
    user = get_current()
    registrations = find_entities(
        user=user,
        interfaces=[IPreregistration])
    len_result = len(registrations)
    index = str(len_result)
    if len_result > 1:
        index = '*'

    view_title = request.localizer.translate(
        _(REGISTRATION_CONTENTS_MESSAGES[index],
          mapping={'nember': len_result}))
    result['removed'] = True
    result['view_title'] = view_title
    return result


#Ideas

def get_archive_idea_metadata(action, request, context, api, **kwargs):
    result = get_edit_entity_metadata(
        action, request,
        context, api,
        _("L'idée a bien été archivée."),
        **kwargs)
    source_path = result.get('source_path')
    view_name = 'seemycontents'
    if result.get('is_excuted') and source_path and \
       not (source_path.find('/@@'+view_name) >= 0 or \
            source_path.find('/'+view_name) >= 0):
        result['removed'] = True
        result['force_remove'] = True

    return result


def get_publish_idea_metadata(action, request, context, api, **kwargs):
    return get_edit_entity_metadata(
        action, request,
        context, api,
        _("L'idée a bien été publiée."),
        **kwargs)


def get_opinion_idea_metadata(action, request, context, api, **kwargs):
    return get_edit_entity_metadata(
        action, request,
        context, api,
        _("L'idée a bien été examinée."),
        **kwargs)


def get_edit_idea_metadata(action, request, context, api, **kwargs):
    return get_edit_entity_metadata(
        action, request,
        context, api,
        _("L'idée a bien été modifiée."),
        **kwargs)


def get_dirct_archive_idea_metadata(action, request, context, api, **kwargs):
    result = get_dirct_edit_entity_metadata(
        action, request,
        context, api,
        _("L'idée a bien été archivée."),
        **kwargs)
    source_path = api.params('source_path')
    view_name = 'seemycontents'
    if source_path and \
       not (source_path.find('/@@'+view_name) >= 0 or \
            source_path.find('/'+view_name) >= 0):
        result['removed'] = True
        result['force_remove'] = True

    return result


def get_dirct_recuperate_idea_metadata(action, request, context, api, **kwargs):
    return get_dirct_edit_entity_metadata(
        action, request,
        context, api,
        _("L'idée a bien été récupérée."),
        **kwargs)


def get_dirct_edit_idea_metadata(action, request, context, api, **kwargs):
    return get_dirct_edit_entity_metadata(
        action, request,
        context, api,
        _("L'idée a bien été modifiée."),
        **kwargs)


def get_remove_idea_metadata(action, request, context, api, **kwargs):
    result = get_edit_entity_metadata(
        action, request, context, api,
        _("L'idée a bien été supprimée."),
        **kwargs)
    result['removed'] = True
    result['force_remove'] = True
    return result


#Organizations

def get_user_edit_organization_metadata(action, request, context, api, **kwargs):
    source_path = api.params('source_path')
    source_context = None
    alert_msg = None
    removed = False
    new_obj_body = None
    redirect_url = None
    body = None
    if 'view_data' in kwargs:
        view_instance, view_result = kwargs['view_data']
        if view_result and view_result is not nothing:
            if isinstance(view_result, HTTPFound):
                alert_msg = _(
                    "Les données associées à l'organisation "
                    "de l'utilisateur ${context} ont bien été"
                    " modifiées.",
                    mapping={
                        'context': context.first_name + ' ' + \
                                   context.last_name})
                if source_path:
                    source_path = '/'.join(source_path.split('/')[:-1])
                    source_context = find_resource(request.root, source_path)
                    if source_context:
                        if isinstance(source_context, Organization) and\
                           context.organization is not source_context:
                            removed = True
                            alert_msg = _(
                                "L'utilisateur ${context} a bien"
                                " changé d'organisation.",
                                mapping={
                                    'context': context.first_name + \
                                               ' ' + context.last_name})
                        elif not isinstance(source_context, Person):
                            if request.POST:
                                request.POST.clear()

                            request.invalidate_cache = True
                            new_obj_body = render_listing_obj(
                                request, context, get_current())
                        else:
                            redirect_url = view_result.headers['location']
            else:
                body = view_result['coordinates'][view_instance.coordinates][0]['body']

    result = {
        'action': 'redirect_action',
        'view': api,
        'redirect_url': redirect_url,
        'removed': removed,
        'view_name': 'index',
        'new_obj_body': new_obj_body,
        'new_body': json.dumps(body) if body else None
    }
    result['alert_msg'] = request.localizer.translate(alert_msg) if alert_msg else None
    result['alert_type'] = 'success'
    return result


def get_edit_organization_metadata(action, request, context, api, **kwargs):
    return get_edit_entity_metadata(
        action, request,
        context, api,
        _("Les données de l'organisation"" ont été mis à jour."),
        **kwargs)


def get_remove_organization_metadata(action, request, context, api, **kwargs):
    result = get_edit_entity_metadata(
        action, request, context, api,
        _("L'organisation a bien été supprimée."),
        'seeorganizations', **kwargs)
    user = get_current()
    registrations = find_entities(
        user=user,
        interfaces=[IOrganization])
    len_result = len(registrations)
    index = str(len_result)
    if len_result > 1:
        index = '*'

    view_title = request.localizer.translate(
        _(ORGANIZATION_CONTENTS_MESSAGES[index],
          mapping={'nember': len_result}))
    result['removed'] = True
    result['view_title'] = view_title
    return result


def get_assigne_roles_user_metadata(action, request, context, api, **kwargs):
    return get_edit_entity_metadata(
        action, request,
        context, api,
        _("Le rôle de l'utilisateur a bien été modifié."),
        **kwargs)


METADATA_GETTERS = {
    'novaideoabstractprocess.select': get_selection_metadata,
    'novaideoabstractprocess.deselect': get_selection_metadata,

    'novaideoviewmanager.contact': get_default_action_metadata,

    'newslettermanagement.subscribe': get_default_action_metadata,

    'channelmanagement.subscribe': get_subscribtion_metadata,
    'channelmanagement.unsubscribe': get_subscribtion_metadata,

    'ideamanagement.creat': get_default_action_metadata,
    'ideamanagement.delidea': get_remove_idea_metadata,
    'ideamanagement.duplicate': get_default_action_metadata,
    'ideamanagement.edit': get_edit_idea_metadata,
    'ideamanagement.archive': get_archive_idea_metadata,
    'ideamanagement.moderationarchive': get_archive_idea_metadata,
    'ideamanagement.abandon': get_dirct_archive_idea_metadata,
    'ideamanagement.recuperate': get_dirct_recuperate_idea_metadata,
    'ideamanagement.publish': get_publish_idea_metadata,
    'ideamanagement.publish_moderation': get_publish_idea_metadata,
    'ideamanagement.makeitsopinion': get_opinion_idea_metadata,
    'ideamanagement.support': get_support_metadata,
    'ideamanagement.oppose': get_support_metadata,
    'ideamanagement.withdraw_token': get_support_metadata,
    'ideamanagement.comment': get_comment_metadata,
    'ideamanagement.present': get_present_metadata,

    'proposalmanagement.support': get_support_metadata,
    'proposalmanagement.oppose': get_support_metadata,
    'proposalmanagement.withdraw_token': get_support_metadata,
    'proposalmanagement.comment': get_comment_metadata,
    'proposalmanagement.present': get_present_metadata,

    'amendmentmanagement.comment': get_comment_metadata,
    'amendmentmanagement.present': get_present_metadata,

    'usermanagement.discuss': get_discuss_metadata,
    'usermanagement.general_discuss': get_general_discuss_metadata,
    'usermanagement.assign_roles': get_assigne_roles_user_metadata,

    'commentmanagement.respond': get_respond_metadata,
    'commentmanagement.remove': get_remove_comment_metadata,
    'commentmanagement.edit': get_edit_comment_metadata,

    'registrationmanagement.remove': get_remove_registration_metadata,
    'registrationmanagement.refuse': get_remove_registration_metadata,
    'registrationmanagement.accept': get_accept_registration_metadata,
    'registrationmanagement.remind': get_remind_registration_metadata,

    'invitationmanagement.edit': get_edit_invitation_metadata,
    'invitationmanagement.remove': get_remove_invitation_metadata,
    'invitationmanagement.reinvite': get_remind_invitation_metadata,
    'invitationmanagement.remind': get_remind_invitation_metadata,

    'organizationmanagement.edit': get_edit_organization_metadata,
    'organizationmanagement.remove': get_remove_organization_metadata,
    'organizationmanagement.withdraw_user': get_withdraw_user_metadata,
    'organizationmanagement.add_members': get_edit_organization_metadata,
    'organizationmanagement.remove_members': get_edit_organization_metadata,
    'organizationmanagement.user_edit_organization': get_user_edit_organization_metadata,
}


def get_all_updated_data(action, request, context, api, **kwargs):
    metadatagetter = METADATA_GETTERS.get(
        action.process_id + '.' + action.node_id, None)
    if metadatagetter:
        return metadatagetter(action, request, context, api, **kwargs)

    return {'action': None, 'view': api}
