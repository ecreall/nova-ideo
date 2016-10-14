import graphene
import graphene.core.types.custom_scalars
from pyramid.threadlocal import get_current_request

from pontus.schema import select
from dace.objectofcollaboration.principal.util import has_role
from dace.util import get_obj, find_catalog, getSite, getAllBusinessAction

from novaideo.content.interface import IPerson
from novaideo.content.idea import Idea as IdeaClass, IdeaSchema


def oth_user(token):
    current_user = None
    request = get_current_request()
    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    identifier_index = novaideo_catalog['api_token']
    object_provides_index = dace_catalog['object_provides']
    query = object_provides_index.any([IPerson.__identifier__]) &\
        identifier_index.eq(token)
    users = list(query.execute().all())
    user = users[0] if users else None
    if (has_role(user=user, role=('SiteAdmin', )) or
            'active' in getattr(user, 'state', [])):
        current_user = user
        request.user = current_user

    return current_user


def get_context(oid):
    try:
        return get_obj(int(oid))
    except:
        return getSite()


def get_action(action_id, context, request):
    node_process = action_id.split('.')
    if len(node_process) == 2:
        process_id, node_id = node_process
        node_actions = getAllBusinessAction(
            context, request,
            process_id=process_id, node_id=node_id,
            process_discriminator='Application')
        if node_actions:
            return node_actions[0]

    return None


def get_execution_data(action_id, args):
    oth_user(args.pop('token'))
    context = get_context(
        args.pop('context') if 'context' in args else None)
    request = get_current_request()
    action = get_action(action_id, context, request)
    return context, request, action, args


class CreateIdea(graphene.Mutation):

    class Input:
        context = graphene.String()
        token = graphene.String()
        title = graphene.String()
        text = graphene.String()
        keywords = graphene.List(graphene.String())

    status = graphene.Boolean()
    idea = graphene.Field('Idea')
    action_id = 'ideamanagement.creat'

    @classmethod
    def mutate(cls, instance, args, info):
        idea_schema = select(
            IdeaSchema(), ['title', 'text', 'keywords'])
        args = dict(args)
        idea_schema.deserialize(args)
        context, request, action, args = get_execution_data(
            cls.action_id, args)
        new_idea = None
        if action:
            new_idea = IdeaClass(**args)
            appstruct = {
                '_object_data': new_idea
            }
            action.execute(context, request, appstruct)

        status = new_idea is not None
        return cls(idea=new_idea, status=status)


class CreateAndPublishIdea(CreateIdea):
    action_id = 'ideamanagement.creatandpublish'


class CreateProposal(CreateIdea):
    action_id = 'ideamanagement.creatandpublishasproposal'


class Mutations(graphene.ObjectType):
    create_idea = graphene.Field(CreateIdea)
    create_publish_idea = graphene.Field(CreateAndPublishIdea)
    create_proposal = graphene.Field(CreateProposal)
