import graphene
import urllib

from dace.util import getSite
from pontus.schema import select

from novaideo.content.person import Preregistration, PersonSchema
from ..util import get_context, get_current_request, get_action
from novaideo import _


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
        args = dict(args)
        context = getSite()
        request = get_current_request()
        action = get_action(Registration.action_id, context, request)
        registration_shema = registration_shema.bind(context=context, request=request)
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
        args = dict(args)
        registration_name = args.get('registration', None)
        root = getSite()
        context = root.get(registration_name, None)
        token = None
        if context and isinstance(context, Preregistration):
            request = get_current_request()
            action = get_action(ConfirmRegistration.action_id, context, request)
            if action:
                preson = action.execute(context, request, {})
                token = preson.api_token
            else:
                raise Exception(
                    request.localizer.translate(_("Authorization failed")))

        status = token is not None
        return ConfirmRegistration(token=token, status=status)


