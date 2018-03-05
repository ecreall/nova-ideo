# -*- coding: utf-8 -*-
import datetime
import pytz
import graphene
from graphene import relay

from pyramid.threadlocal import get_current_request
from substanced.objectmap import find_objectmap
from substanced.util import get_oid

from dace.util import get_obj

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
from .interfaces import IEntity
from .util import get_user_by_token, get_entities, get_all_comments, get_actions, connection_for_type, get_context


class Node(object):

    @classmethod
    def get_node(cls, id, context, info):  #pylint: disable=W0613,W0622
        oid = int(id)
        return get_obj(oid)


class Debatable(graphene.AbstractType):

    channel = graphene.Field(lambda: Channel)
    comments = relay.ConnectionField(
        lambda: Comment,
        filter=graphene.String())
    len_comments = graphene.Int()

    def resolve_channel(self, args, context, info):
        if not hasattr(self, 'get_channel'):
            return None

        return self.get_channel(getattr(context, 'user', None))

    def resolve_comments(self, args, context, info):
        if not hasattr(self, 'get_channel'):
            return []

        channel = self.get_channel(getattr(context, 'user', None))
        total_count, oids = get_all_comments(channel, args)
        return ResolverLazyList(
            oid,
            Comment,
            total_count=total_count)

    def resolve_len_comments(self, args, context, info):
        if not hasattr(self, 'get_channel'):
            return 0

        channel = self.get_channel(getattr(context, 'user', None))
        return channel.len_comments if channel else 0
 

class Emoji(Node, graphene.ObjectType):
    
    class Meta(object):
        interfaces = (relay.Node, )
    
    users = graphene.List(lambda: Person)
    title = graphene.String()
    is_user_emoji = graphene.Boolean()
    
    def resolve_users(self, args, context, info):
        return ResolverLazyList(self.users, Person)


class Emojiable(graphene.AbstractType):

    emojis = graphene.List(Emoji)
    user_emoji = graphene.String()

    def resolve_emojis(self, args, context, info):
        user_emoji = self.get_user_emoji(getattr(context, 'user', None))
        return [Emoji(title=title, users=users, is_user_emoji=user_emoji==title)
                for title, users in self.emojis.items()]

    def resolve_user_emoji(self, args, context, info):
        return self.get_user_emoji(getattr(context, 'user', None))


class Root(Node, Debatable, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, IEntity)

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
    logo = graphene.Field(lambda: File)

    def resolve_site_id(self, args, context, info):  # pylint: disable=W0613
        # TODO return the site id exp: evolutions...
        return "default"

    def resolve_logo(self, args, context, info):  # pylint: disable=W0613
        return self.picture

    def resolve_keywords_required(self, args, context, info):  # pylint: disable=W0613
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


class File(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    url = graphene.String()
    mimetype = graphene.String()
    is_image = graphene.Boolean()
    variations = graphene.List(graphene.String)

    def resolve_is_image(self, args, context, info):  #pylint: disable=W0613
        return self.mimetype.startswith('image') or \
            self.mimetype.startswith(
                'application/x-shockwave-flash')

    def resolve_variations(self, args, context, info):  #pylint: disable=W0613
        return list(self.keys())


class Person(Node, Debatable, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    function = graphene.String()
    description = graphene.String()
    picture = graphene.Field(File)
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

#    email = graphene.String()
#    email should be visible only by user with Admin or Site Administrator role
    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, (SDPerson, SDBot, SDMask))

    def resolve_is_anonymous(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, 'is_anonymous', False)

    def resolve_contents(self, args, context, info):  # pylint: disable=W0613
        contents = self.get_contents(context.user) \
            if hasattr(self, 'get_contents') else getattr(self, 'contents', [])
        user_ideas = [get_oid(o) for o in contents]
        total_count, oids = get_entities([Iidea], [], args, info, user=context.user, intersect=user_ideas)
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


Person.Connection = connection_for_type(Person)


class Url(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, )

    url = graphene.String()
    domain = graphene.String()
    title = graphene.String()
    description = graphene.String()
    image_url = graphene.String()
    site_name = graphene.String()
    favicon = graphene.String()
    image = graphene.Field(File)
    author_avatar = graphene.String()
    author_name = graphene.String()


class Comment(Node, Emojiable, graphene.ObjectType):

    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    state = graphene.List(graphene.String)
    text = graphene.String()
    author = graphene.Field(Person)
    attached_files = graphene.List(File)
    urls = graphene.List(Url)
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

    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, SDComment)

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
        return getattr(self, 'formatted_comment', self.comment)

    def resolve_urls(self, args, context, info):  # pylint: disable=W0613
        return [Url(**url) for url in getattr(self, 'urls', {}).values()]

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


class Idea(Node, Debatable, graphene.ObjectType):

    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, IEntity)

    presentation_text = graphene.String()
    text = graphene.String()
    keywords = graphene.List(graphene.String)
    author = graphene.Field(Person)
    tokens_opposition = graphene.Int()
    tokens_support = graphene.Int()
    attached_files = graphene.List(File)
    user_token = graphene.String()
    urls = graphene.List(Url)
    opinion = graphene.String()
    
    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, SDIdea)

    def resolve_presentation_text(self, args, context, info):
        return self.presentation_text(300)

    def resolve_tokens_opposition(self, args, context, info):  # pylint: disable=W0613
        return self.len_opposition

    def resolve_tokens_support(self, args, context, info):  # pylint: disable=W0613
        return self.len_support

    def resolve_urls(self, args, context, info):  # pylint: disable=W0613
        return [Url(**url) for url in getattr(self, 'urls', {}).values()]

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


class ResolverLazyList(object):

    def __init__(self, origin, object_type, state=None, total_count=None):
        self._origin = origin
        self._state = state or []
        self._origin_iter = None
        self._total_count = total_count
        self._finished = False
        objectmap = find_objectmap(get_current_request().root)
        self.resolver = objectmap.object_for
        self.object_type = object_type

    def __iter__(self):
        return self if not self._finished else iter(self._state)

    def iter(self):
        return self.__iter__()

    def __len__(self):
        return self._origin.__len__()

    def __next__(self):
        try:
            if not self._origin_iter:
                self._origin_iter = self._origin.__iter__()
            # n = next(self._origin_iter)
            oid = next(self._origin_iter)
            n = self.resolver(oid)
        except StopIteration as e:
            self._finished = True
            raise e
        else:
            self._state.append(n)
            return n

    def next(self):
        return self.__next__()

    def __getitem__(self, key):
        item = self._origin[key]
        if isinstance(key, slice):
            return self.__class__(item, object_type=self.object_type)

        return item

    def __getattr__(self, name):
        return getattr(self._origin, name)

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, repr(self._origin))

    @property
    def total_count(self):
        return self._total_count


class Query(graphene.ObjectType):

    node = relay.Node.Field()
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

    def resolve_ideas(self, args, context, info):  # pylint: disable=W0613
        total_count, oids = get_entities([Iidea], ['published'], args, info)
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
