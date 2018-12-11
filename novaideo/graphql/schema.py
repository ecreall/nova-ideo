# -*- coding: utf-8 -*-
import datetime
import pytz
import graphene
from graphene import relay

from pyramid.threadlocal import get_current_request
from substanced.objectmap import find_objectmap
from substanced.util import get_oid

from dace.objectofcollaboration.principal.role import DACE_ROLES
from dace.util import get_obj
from dace.objectofcollaboration.principal.util import has_role, get_current, get_roles

from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.person import Person as SDPerson
from novaideo.content.mask import Mask as SDMask
from novaideo.content.bot import Bot as SDBot
from novaideo.content.idea import Idea as SDIdea
from novaideo.content.comment import Comment as SDComment
from novaideo.core import Channel as SDChannel
from novaideo.content.interface import Iidea, IPerson
from novaideo.utilities.util import html_to_text
from novaideo import log
from .mutations import Mutations
from .interfaces import IEntity, IDebatable
from .types import SecureObjectType
from .util import (
    get_user_by_token, get_entities, get_all_comments,
    get_actions, connection_for_type, get_context,
    ResolverLazyList)
from novaideo.utilities.util import get_object_examination_stat, get_object_evaluation_stat
from novaideo.role import get_authorized_roles



url_data_keys = [
    'url',
    'html',
    'title',
    'description',
    'thumbnail_url',
    'provider_name',
    'favicon_url',
    'author_name',
    'author_avatar',
    'data'
]


def extract_url_metadata(url_metadata):
    result = {}
    for key in url_data_keys:
        result[key] = url_metadata.get(key, None)

    return result


class Node(object):

    @classmethod
    def get_node(cls, id, context, info):  #pylint: disable=W0613,W0622
        oid = int(id)
        return get_obj(oid)


class UrlData(graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, )

    label = graphene.String()
    data = graphene.String()


class Url(graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, )

    url = graphene.String()
    html = graphene.String()
    title = graphene.String()
    description = graphene.String()
    thumbnail_url = graphene.String()
    provider_name = graphene.String()
    favicon_url = graphene.String()
    author_name = graphene.String()
    author_avatar = graphene.String()
    data = graphene.List(UrlData)

    def resolve_data(self, args, context, info):  # pylint: disable=W0613
        return [UrlData(**entry) for entry in self.data]


class ExaminationStats(Node, graphene.ObjectType):
    
    class Meta(object):
        interfaces = (relay.Node, )
    
    favorable = graphene.Int()
    unfavorable = graphene.Int()
    toStudy = graphene.Int()
    
    def resolve_favorable(self, args, context, info):
        stats = get_object_examination_stat(self, context)
        if not stats: return 0
        return stats['favorable']['value']
    
    def resolve_unfavorable(self, args, context, info):
        stats = get_object_examination_stat(self, context)
        if not stats: return 0
        return stats['unfavorable']['value']

    def resolve_toStudy(self, args, context, info):
        stats = get_object_examination_stat(self, context)
        if not stats: return 0
        return stats['to_study']['value']


class EvaluationStats(Node, graphene.ObjectType):
    
    class Meta(object):
        interfaces = (relay.Node, )
    
    opposition = graphene.Int()
    support = graphene.Int()
    
    def resolve_opposition(self, args, context, info):
        stats = get_object_evaluation_stat(self, context)
        if not stats: return 0
        return stats['opposition']['value']
    
    def resolve_support(self, args, context, info):
        stats = get_object_evaluation_stat(self, context)
        if not stats: return 0
        return stats['support']['value']


class Emoji(Node, graphene.ObjectType):
    
    class Meta(object):
        interfaces = (relay.Node, )
    
    users = relay.ConnectionField(lambda: Person)
    title = graphene.String()
    is_user_emoji = graphene.Boolean()
    
    def resolve_users(self, args, context, info):
        return ResolverLazyList(self.users, Person, total_count=len(self.users))


class Emojiable(graphene.AbstractType):

    emojis = graphene.List(Emoji)
    user_emoji = graphene.String()

    def resolve_emojis(self, args, context, info):
        user_emoji = self.get_user_emoji(getattr(context, 'user', None))
        return [Emoji(title=title, users=users, is_user_emoji=user_emoji==title)
                for title, users in self.emojis.items()]

    def resolve_user_emoji(self, args, context, info):
        return self.get_user_emoji(getattr(context, 'user', None))


class ExaminationDate(graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, )

    start = graphene.String()
    end = graphene.String()


class Root(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, IEntity, IDebatable)

    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, NovaIdeoApplication)

    site_id = graphene.String()
    title = graphene.String()
    keywords_required = graphene.Boolean()
    keywords = graphene.List(graphene.String)
    can_add_keywords = graphene.Boolean()
    anonymisation = graphene.Boolean()
    moderate_proposals = graphene.Boolean()
    moderate_ideas = graphene.Boolean()
    examine_proposals = graphene.Boolean()
    examine_ideas = graphene.Boolean()
    support_proposals = graphene.Boolean()
    support_ideas = graphene.Boolean()
    manage_challenges = graphene.Boolean()
    manage_questions = graphene.Boolean()
    manage_proposals = graphene.Boolean()
    only_invitation = graphene.Boolean()
    only_for_members = graphene.Boolean()
    logo = graphene.Field(lambda: File)
    roles = graphene.List(graphene.String)
    examination_dates = graphene.List(ExaminationDate)

    def resolve_examination_dates(self, args, context, info):
        dates = [d.isoformat() for d in self.deadlines]
        allDates = [d.isoformat() for d in self.deadlines]
        allDates.insert(0, self.created_at.isoformat())
        return [ExaminationDate(start=start, end=end) for start, end in zip(allDates, dates)]

    def resolve_roles(self, args, context, info):  # pylint: disable=W0613
        roles = get_authorized_roles(context.user)
        return [key for key in roles.keys() if not DACE_ROLES[key].islocal]

    def resolve_site_id(self, args, context, info):  # pylint: disable=W0613
        # TODO return the site id exp: evolutions...
        return "default"

    def resolve_logo(self, args, context, info):  # pylint: disable=W0613
        return self.picture

    def resolve_keywords_required(self, args, context, info):  # pylint: disable=W0613
        return False

    def resolve_only_for_members(self, args, context, info):  # pylint: disable=W0613
        # TODO return the site id exp: evolutions...
        return False


class Action(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    process_id = graphene.String()
    node_id = graphene.String()
    behavior_id = graphene.String()
    counter = graphene.Int()
    style = graphene.String()
    descriminator = graphene.String()
    tags = graphene.List(graphene.String)
    icon = graphene.String()
    order = graphene.Int()
    submission_title = graphene.String()
    description = graphene.String()
    active = graphene.Boolean()

    def resolve_title(self, args, context, info):  # pylint: disable=W0613
        return context.localizer.translate(self.action.title)

    def resolve_description(self, args, context, info):  # pylint: disable=W0613
        return context.localizer.translate(self.action.description)

    def resolve_tags(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'tags', [])

    def resolve_submission_title(self, args, context, info):  # pylint: disable=W0613
        submission_title = getattr(self.action, 'submission_title', '')
        return context.localizer.translate(submission_title) if submission_title else submission_title

    def resolve_counter(self, args, context, info):  # pylint: disable=W0613
        try:
            action = self.action
            if hasattr(action, 'get_title'):
                return action.get_title(self.context, context, True)
        except Exception as e:
            return None

        return None

    def resolve_process_id(self, args, context, info):  # pylint: disable=W0613
        return self.action.process_id

    def resolve_node_id(self, args, context, info):  # pylint: disable=W0613
        return self.action.node_id

    def resolve_behavior_id(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'behavior_id', self.action.__class__.__name__)

    def resolve_style(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'style', '')

    def resolve_descriminator(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'style_descriminator', '')

    def resolve_icon(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'style_picto', '')

    def resolve_order(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'style_order', 100)

    def resolve_active(self, args, context, info):  # pylint: disable=W0613
        is_active = getattr(self.action, 'is_active', None)
        return False if not is_active else self.action.is_active(self.context, context)


class File(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    url = graphene.String()
    mimetype = graphene.String()
    is_image = graphene.Boolean()
    variations = graphene.List(graphene.String)
    size = graphene.Int()

    def resolve_is_image(self, args, context, info):  #pylint: disable=W0613
        return self.mimetype.startswith('image') or \
            self.mimetype.startswith(
                'application/x-shockwave-flash')

    def resolve_variations(self, args, context, info):  #pylint: disable=W0613
        return list(self.keys())

    def resolve_size(self, args, context, info):  #pylint: disable=W0613
        return self.get_size()


class Person(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, IEntity, IDebatable)

    function = graphene.String()
    description = graphene.String()
    picture = graphene.Field(File)
    cover_picture = graphene.Field(File)
    first_name = graphene.String()
    last_name = graphene.String()
    user_title = graphene.String()
    locale = graphene.String()
    contents = relay.ConnectionField(
        lambda: Idea,
        filter=graphene.String()
    )
    followed_ideas = relay.ConnectionField(
        lambda: Idea,
        filter=graphene.String()
    )
    supported_ideas = relay.ConnectionField(
        lambda: Idea,
        filter=graphene.String()
    )
    channels = relay.ConnectionField(lambda: Channel)
    discussions = relay.ConnectionField(lambda: Channel)
    available_tokens = graphene.Int()
    is_anonymous = graphene.Boolean()
    mask = graphene.Field(lambda: Person)
#   email should be visible only by user with Admin or Site Administrator role
    email = graphene.String()
    api_token = graphene.String()
    roles = graphene.List(graphene.String)

    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, (SDPerson, SDBot, SDMask))

    def resolve_roles(self, args, context, info):  # pylint: disable=W0613
        return [r for r in get_roles(self)
                if not getattr(DACE_ROLES.get(r, None), 'islocal', False)]

    def resolve_is_anonymous(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, 'is_anonymous', False)

    def resolve_contents(self, args, context, info):  # pylint: disable=W0613
        user = get_current(context)
        contents = self.get_contents(user) \
            if hasattr(self, 'get_contents') else getattr(self, 'contents', [])
        user_ideas = [get_oid(o) for o in contents]
        total_count, oids = get_entities([Iidea], ['published', 'to work', 'draft'], args, info, user=user, intersect=user_ideas)
        return ResolverLazyList(oids, Idea, total_count=total_count)

    def resolve_followed_ideas(self, args, context, info):  # pylint: disable=W0613
        user_ideas = [get_oid(o) for o in getattr(self, 'selections', [])]
        total_count, oids = get_entities([Iidea], ['published'], args, info, intersect=user_ideas)
        return ResolverLazyList(oids, Idea, total_count=total_count)

    def resolve_supported_ideas(self, args, context, info):  # pylint: disable=W0613
        user_ideas = self.evaluated_objs_ids() if hasattr(self, 'evaluated_objs_ids') else []
        total_count, oids = get_entities([Iidea], ['published'], args, info, intersect=user_ideas)
        return ResolverLazyList(oids, Idea, total_count=total_count)

    def resolve_channels(self, args, context, info):  # pylint: disable=W0613
        channels = sorted(
            [c for c in getattr(self, 'following_channels', [])
             if not c.is_discuss() and isinstance(c.subject, SDIdea)],
            key=lambda e: getattr(e, 'created_at'), reverse=True)
        channels.insert(0, context.root.channel)
        return channels

    def resolve_discussions(self, args, context, info):  # pylint: disable=W0613
        return sorted(
            [c for c in getattr(self, 'following_channels', [])
             if c.is_discuss()],
            key=lambda e: getattr(e, 'created_at'), reverse=True)

    def resolve_available_tokens(self, args, context, info):  # pylint: disable=W0613
        if hasattr(self, 'get_len_free_tokens'):
            return self.get_len_free_tokens(context.root, True)
        
        return 0

    def resolve_email(self, args, context, info):  # pylint: disable=W0613
        user = context.user
        return self.email if user and (user is self or has_role(user=user, role=('PortalManager',))) else None

    def resolve_api_token(self, args, context, info):  # pylint: disable=W0613
        user = context.user
        return self.api_token if user and (user is self or has_role(user=user, role=('PortalManager',))) else None

    def resolve_mask(self, args, context, info):  # pylint: disable=W0613
        return self.get_mask(context.root)


Person.Connection = connection_for_type(Person)


class Comment(Node, Emojiable, graphene.ObjectType):

    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    state = graphene.List(graphene.String)
    text = graphene.String()
    author = graphene.Field(Person)
    attached_files = graphene.List(File)
    oid = graphene.String()
    comments = relay.ConnectionField(
        lambda: Comment,
        filter=graphene.String())
    len_comments = graphene.Int()
    root_oid = graphene.String()
    channel = graphene.Field(lambda: Channel)
    edited = graphene.Boolean()
    pinned = graphene.Boolean()
    unread_replies = graphene.List(lambda: Comment)
    len_unread_replies = graphene.Int()
    urls = graphene.List(Url)

    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, SDComment)

    def resolve_urls(self, args, context, info):
        urls = getattr(self, 'urls', [])
        return [Url(**extract_url_metadata(url_metadata)) for url_metadata in urls]

    def resolve_unread_replies(self, args, context, info):
        if not context.user:
            return []

        now = datetime.datetime.now(tz=pytz.UTC)
        return ResolverLazyList(
            self.get_comments_between(
                context.user.get_read_date(self, self.created_at), now), Comment)

    def resolve_len_unread_replies(self, args, context, info):
        if not context.user:
            return 0

        now = datetime.datetime.now(tz=pytz.UTC)
        return len(self.get_comments_between(
                context.user.get_read_date(self, self.created_at), now))

    def resolve_text(self, args, context, info):
        return self.comment

    def resolve_oid(self, args, context, info):  # pylint: disable=W0613
        return get_oid(self, None)

    def resolve_attached_files(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, 'files', [])

    def resolve_comments(self, args, context, info):  # pylint: disable=W0613
        total_count, oids = get_all_comments(self, args)
        return ResolverLazyList(
            oids,
            Comment,
            total_count=total_count)

    def resolve_len_comments(self, args, context, info):
        return self.len_comments

    def resolve_root_oid(self, args, context, info):  # pylint: disable=W0613
        return get_oid(self.channel.get_subject(getattr(context, 'user', None)), None)


Comment.Connection = connection_for_type(Comment)


class Channel(Node, graphene.ObjectType):

    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    comments = relay.ConnectionField(
        Comment,
        pinned=graphene.Boolean(),
        file=graphene.Boolean(),
        filter=graphene.String())
    members = relay.ConnectionField(
        Person,
        filter=graphene.String())
    subject = graphene.Field(lambda: EntityUnion)
    unread_comments = graphene.List(Comment)
    len_unread_comments = graphene.Int()
    len_comments = graphene.Int()
    is_discuss = graphene.Boolean()
    
    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, SDChannel)

    def resolve_members(self, args, context, info):  # pylint: disable=W0613
        oids = [get_oid(m) for m in self.members]
        total_count = len(self.members)
        return ResolverLazyList(oids, Person, total_count=total_count)

    def resolve_comments(self, args, context, info):
        total_count, oids = get_all_comments(self, args)
        return ResolverLazyList(
            oids,
            Comment,
            total_count=total_count)

    def resolve_unread_comments(self, args, context, info):
        if not context.user:
            return []

        now = datetime.datetime.now(tz=pytz.UTC)
        return ResolverLazyList(
            self.get_comments_between(
                context.user.get_read_date(self), now), Comment)

    def resolve_len_unread_comments(self, args, context, info):
        if not context.user:
            return 0

        now = datetime.datetime.now(tz=pytz.UTC)
        return len(self.get_comments_between(
                context.user.get_read_date(self), now))

    def resolve_subject(self, args, context, info):  # pylint: disable=W0613
        return self.get_subject(getattr(context, 'user', None))

    def resolve_title(self, args, context, info):  # pylint: disable=W0613
        return context.localizer.translate(self.get_title(context.user))

    def resolve_is_discuss(self, args, context, info):  # pylint: disable=W0613
        return self.is_discuss()


Channel.Connection = connection_for_type(Channel)


class Idea(SecureObjectType, Node, graphene.ObjectType):

    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, IEntity, IDebatable)

    presentation_text = graphene.String()
    text = graphene.String()
    keywords = graphene.List(graphene.String)
    author = graphene.Field(Person)
    tokens_opposition = graphene.Int()
    tokens_support = graphene.Int()
    attached_files = graphene.List(File)
    user_token = graphene.String()
    opinion = graphene.String()
    urls = graphene.List(Url)

    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, SDIdea)

    def resolve_urls(self, args, context, info):
        urls = getattr(self, 'urls', [])
        return [Url(**extract_url_metadata(url_metadata)) for url_metadata in urls]

    def resolve_presentation_text(self, args, context, info):
        return self.presentation_text(300)

    def resolve_tokens_opposition(self, args, context, info):  # pylint: disable=W0613
        return self.len_opposition

    def resolve_tokens_support(self, args, context, info):  # pylint: disable=W0613
        return self.len_support

    def resolve_user_token(self, args, context, info):  # pylint: disable=W0613
        return self.evaluation(context.user)

    def resolve_opinion(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, 'opinion', {}).get('explanation', '')


Idea.Connection = connection_for_type(Idea)


class EntityUnion(graphene.Union):
    class Meta:
        types = (Idea, Root, Person) # TODO add Question...

    @classmethod
    def resolve_type(cls, instance, context, info):
        if isinstance(instance, SDIdea):
            return Idea

        if isinstance(instance, NovaIdeoApplication):
            return Root

        if isinstance(instance, SDPerson):
            return Person

        raise Exception()


class EntityData(Node, graphene.ObjectType):
    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    channel = graphene.Field(lambda: Channel)
    subject = graphene.Field(lambda: EntityUnion)

    def resolve_channel(self, args, context, info):
        user = getattr(context, 'user', None)
        if not hasattr(self, 'get_channel') or user is self: return None
        return self.get_channel(getattr(context, 'user', None))

    def resolve_subject(self, args, context, info):
        return self
 

EntityData.Connection = connection_for_type(EntityData)


class Query(graphene.ObjectType):

    node = relay.Node.Field()
    members = relay.ConnectionField(
        Person,
        filter=graphene.String()
    )
    ideas = relay.ConnectionField(
        Idea,
        filter=graphene.String()
    )
    account = graphene.Field(Person)
    actions = relay.ConnectionField(
        Action,
        action_tags=graphene.List(graphene.String),
        process_tags=graphene.List(graphene.String),
        process_ids=graphene.List(graphene.String),
        node_ids=graphene.List(graphene.String),
        context=graphene.String()
    )
    root = graphene.Field(Root)
    all_channels = relay.ConnectionField(
        EntityData,
        filter=graphene.String()
    )
    all_contents = relay.ConnectionField(
        EntityData,
        filter=graphene.String()
    )

    def resolve_ideas(self, args, context, info):  # pylint: disable=W0613
        user = get_current(context)
        total_count, oids = get_entities([Iidea], ['published', 'to work', 'draft'], args, info, user=user)
        return ResolverLazyList(oids, Idea, total_count=total_count)

    def resolve_members(self, args, context, info):  # pylint: disable=W0613
        user = get_current(context)
        total_count, oids = get_entities([IPerson], ['active'], args, info, user=user)
        return ResolverLazyList(oids, Person, total_count=total_count)

    def resolve_all_channels(self, args, context, info):  # pylint: disable=W0613
        user = get_current(context)
        total_count, oids = get_entities([Iidea, IPerson], ['published', 'active'], args, info, user=user)
        return ResolverLazyList(oids, EntityData, total_count=total_count)

    def resolve_all_contents(self, args, context, info):  # pylint: disable=W0613
        # todo add questions...
        user = get_current(context)
        total_count, oids = get_entities([Iidea], ['published', 'to work', 'draft', 'active'], args, info, user=user)
        return ResolverLazyList(oids, Idea, total_count=total_count)

    def resolve_account(self, args, context, info):  # pylint: disable=W0613
        return context.user

    def resolve_actions(self, args, context, info):  # pylint: disable=W0613
        return get_actions(get_context(args.get('context', '')), context, args)

    def resolve_root(self, args, context, info):  # pylint: disable=W0613
        return context.root


schema = graphene.Schema(query=Query, mutation=Mutations)


if __name__ == '__main__':
    import json
    schema_dict = {'data': schema.introspect()}
    with open('schema.json', 'w') as outfile:
        json.dump(schema_dict, outfile)
