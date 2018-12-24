import graphene
from graphene import relay

from substanced.util import find_service
from substanced.interfaces import UserToPasswordReset
from substanced.objectmap import find_objectmap

from dace.objectofcollaboration.principal.role import DACE_ROLES
from dace.objectofcollaboration.principal.util import get_roles
from dace.util import getSite, get_obj
from pontus.schema import select

from novaideo.content.person import Preregistration, PersonSchema
from novaideo.content.processes.user_management.behaviors import (
    send_reset_password)
from novaideo import _
from ..util import (
    get_current_request, get_action,
    extract_files, get_execution_data)
from . import Upload


class ThemePreferencesInput(graphene.InputObjectType):
    primary_color = graphene.String(required=False)
    secondary_color = graphene.String(required=False)


class PreferencesInput(graphene.InputObjectType):
    theme = ThemePreferencesInput(required=False)


class Registration(graphene.Mutation):

    class Input:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    status = graphene.Boolean()
    action_id = 'registrationmanagement.registration'

    @staticmethod
    def mutate(root, args, context, info):
        registration_shema = select(
            PersonSchema(), ['first_name', 'last_name', 'email', 'password'])
        context = getSite()
        request = get_current_request()
        action = get_action(Registration.action_id, context, request)
        registration_shema = registration_shema.bind(
            context=context, request=request)
        args = registration_shema.deserialize(args)
        preregistration = None
        if action:
            preregistration = Preregistration(**args)
            appstruct = {
                '_object_data': preregistration
            }
            action.execute(context, request, appstruct)
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        status = preregistration is not None
        return Registration(status=status)


class ConfirmRegistration(graphene.Mutation):

    class Input:
        registration = graphene.String()

    status = graphene.Boolean()
    token = graphene.String()
    action_id = 'registrationmanagement.confirmregistration'

    @staticmethod
    def mutate(root, args, context, info):
        registration_name = args.get('registration', None)
        root = getSite()
        context = root.get(registration_name, None)
        token = None
        if context and isinstance(context, Preregistration):
            request = get_current_request()
            action = get_action(ConfirmRegistration.action_id, context, request)
            if action:
                person = action.execute(context, request, {})
                token = person.api_token
            else:
                raise Exception(
                    request.localizer.translate(_("Authorization failed")))

        status = token is not None
        return ConfirmRegistration(token=token, status=status)


class EditProfile(graphene.Mutation):

    class Input:
        context = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        function = graphene.String()
        description = graphene.String()
        locale = graphene.String()
        picture = graphene.List(Upload)
        cover_picture = graphene.List(Upload)
        old_picture = graphene.String()
        old_cover = graphene.String()

    status = graphene.Boolean()
    profile = graphene.Field('novaideo.graphql.schema.Person')
    action_id = 'usermanagement.edit'

    @staticmethod
    def mutate(root, args, context, info):
        person_schema = select(
            PersonSchema(),
            ['first_name', 'last_name', 'email', 'function',
             'description', 'locale', 'cover_picture', 'picture'])
        args = dict(args)
        request = get_current_request()
        old_picture = args.pop('old_picture', None)
        old_cover = args.pop('old_cover', None)
        files = extract_files('picture', request)
        picture = files[0] if files else None
        files = extract_files('cover_picture', request)
        cover_picture = files[0] if files else None
        if picture:
            args['picture'] = picture
        else:
            args.pop('picture')

        if cover_picture:
            args['cover_picture'] = cover_picture
        else:
            args.pop('cover_picture')

        context = get_obj(int(args.pop('context')))
        action = get_action(EditProfile.action_id, context, request)
        person_schema = person_schema.bind(context=context, request=request)
        args = person_schema.deserialize(args)
        args['cover_picture'] = args['cover_picture'] and args['cover_picture']['_object_data']
        args['picture'] = args['picture'] and args['picture']['_object_data']
        status = False
        if action:
            picture = args.pop('picture')
            cover_picture = args.pop('cover_picture')
            if not old_picture: context.setproperty('picture', picture)
            if not old_cover: context.setproperty('cover_picture', cover_picture)
            context.set_data(args)
            action.execute(context, request, args)
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return EditProfile(profile=context, status=status)


class EditPassword(graphene.Mutation):

    class Input:
        context = graphene.String()
        current_password = graphene.String()
        password = graphene.String()

    status = graphene.Boolean()
    action_id = 'usermanagement.edit_password'

    @staticmethod
    def mutate(root, args, context, info):
        person_schema = select(
            PersonSchema(), ['password'])
        context_oid = args.pop('context')
        current_password = args.pop('current_password')
        args = person_schema.deserialize(dict(args))
        args['context'] = context_oid
        args['current_password'] = current_password
        context, request, action, args = get_execution_data(
            EditPassword.action_id, args)
        status = False
        if action:
            result = action.execute(context, request, args)
            status = result.get('edited', False)
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return EditPassword(status=status)


class EditApiToken(graphene.Mutation):

    class Input:
        context = graphene.String()
        password = graphene.String()

    status = graphene.Boolean()
    api_token = graphene.String()
    action_id = 'usermanagement.get_api_token'

    @staticmethod
    def mutate(root, args, context, info):
        person_schema = select(
            PersonSchema(), ['password'])
        context_oid = args.pop('context')
        args = person_schema.deserialize(dict(args))
        args['context'] = context_oid
        context, request, action, args = get_execution_data(
            EditApiToken.action_id, args)
        status = False
        api_token = ''
        if action:
            result = action.execute(context, request, args)
            api_token = result.get('api_token', '')
            status = True if api_token else False
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return EditApiToken(status=status, api_token=api_token)


class AssignRoles(graphene.Mutation):

    class Input:
        context = graphene.String()
        roles = graphene.List(graphene.String)

    status = graphene.Boolean()
    roles = graphene.List(graphene.String)
    action_id = 'usermanagement.assign_roles'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            AssignRoles.action_id, args)
        status = False
        user_roles = []
        if action:
            action.execute(context, request, args)
            user_roles = [r for r in get_roles(context)
                          if not getattr(DACE_ROLES.get(r, None), 'islocal', False)]
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return AssignRoles(status=status, roles=user_roles)


class Activate(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    profile = graphene.Field('novaideo.graphql.schema.Person')
    action_id = 'usermanagement.activate'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            Activate.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            request.invalidate_cache = True
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Activate(status=status, profile=context)


class Deactivate(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    profile = graphene.Field('novaideo.graphql.schema.Person')
    action_id = 'usermanagement.deactivate'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            Deactivate.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            request.invalidate_cache = True
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Deactivate(status=status, profile=context)


class ResetPassword(graphene.Mutation):

    class Input:
        email = graphene.String()

    status = graphene.Boolean()

    @staticmethod
    def mutate(root, args, context, info):
        reset = None
        request = get_current_request()
        if args.get('email', None):
            reset = send_reset_password(args['email'], request)
        else:
            raise Exception(
                request.localizer.translate(_("Reset password failed")))

        status = reset is not None
        return ResetPassword(status=status)


class ConfirmResetPassword(graphene.Mutation):

    class Input:
        context = graphene.String()
        password = graphene.String()

    token = graphene.String()

    @staticmethod
    def mutate(root, args, context, info):
        reset_name = args.get('context', None)
        root = getSite()
        principals = find_service(root, 'principals')
        context = principals['resets'].get(reset_name, None)
        request = get_current_request()
        localizer = request.localizer
        if not context:
           raise Exception(
                localizer.translate(_("Invalid reset request")))

        person_schema = select(
            PersonSchema(), ['password'])
        args = person_schema.deserialize(dict(args))
        token = None
        if context:
            objectmap = find_objectmap(root)
            users = objectmap.sourceids(context, UserToPasswordReset)
            if users:
                context.reset_password(args['password'])
                person = get_obj(users[0])
                token = person.api_token
        else:
            raise Exception(
                localizer.translate(_("Reset password failed")))

        return ConfirmResetPassword(token=token)


class MarkAlertsAsRead(graphene.Mutation):

    class Input:
        userId = graphene.ID()
        alerts = graphene.List(graphene.ID)

    status = graphene.Boolean()

    @staticmethod
    def mutate(root, args, context, info):
        alertsIds = args.get('alerts', [])
        userId = args.get('userId', None)
        if alertsIds and userId:
            alerts = [get_obj(int(relay.Node.from_global_id(alert)[1]))
                      for alert in alertsIds]
            user = get_obj(int(relay.Node.from_global_id(userId)[1]))
            if alerts and user:
                for alert in alerts:
                    alert.unsubscribe(user)

        return MarkAlertsAsRead(status=True)


class EditPreferences(graphene.Mutation):

    class Input:
        context = graphene.String()
        preferences = PreferencesInput()

    profile = graphene.Field('novaideo.graphql.schema.Person')
    action_id = 'usermanagement.edit_preferences'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            EditPreferences.action_id, args)
        if action:
            action.execute(context, request, args.get('preferences', {}))
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return EditPreferences(profile=context)
