# -*- coding: utf-8 -*-
import datetime
import pytz
import graphene
from graphene import relay
from graphql_relay.connection.arrayconnection import cursor_to_offset

from hypatia.interfaces import STABLE
from pyramid.threadlocal import get_current_request
from substanced.objectmap import find_objectmap
from substanced.util import get_oid

from dace.util import get_obj, find_catalog, getAllBusinessAction
from dace.objectofcollaboration.entity import ActionCall

from novaideo.views.filter import find_entities
from novaideo.content.idea import Idea as SDIdea
from novaideo.content.comment import Comment as SDComment
from novaideo.content.interface import Iidea, IPerson
from novaideo.utilities.util import html_to_text
from novaideo import log
from novaideo.views.filter import get_comments
from .mutations import Mutations, get_context


def get_user_by_token(token):
    current_user = None
    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    identifier_index = novaideo_catalog['api_token']
    object_provides_index = dace_catalog['object_provides']
    query = object_provides_index.any([IPerson.__identifier__]) &\
        identifier_index.eq(token)
    users = list(query.execute().all())
    return users[0] if users else None


def get_entities(interfaces, states, args, info, intersect=None):  #pylint: disable=W0613
    try:
        after = cursor_to_offset(args.get('after'))
        first = args.get('first')
        if after is None:
            limit = first
        else:
            limit = after + 1 + first

        limit = limit + 1  # retrieve one more so the hasNextPage works
    except Exception:  # FIXME:
        limit = None

    # For the scrolling of the results, it's important that the sort is stable.
    # release_date is set to datetime.datetime.now(tz=pytz.UTC) when the event
    # is published, so we have microsecond resolution and so have a stable sort
    # even with not stable sort algorithms like nbest (because it's unlikely
    # we have several events with the same date).
    # When we specify limit in the query, the sort algorithm chosen will
    # most likely be nbest instead of stable timsort (python sorted).
    # The sort is ascending, meaning we will get new events published during
    # the scroll, it's ok.
    # The only issue we can found here is if x events are removed or unpublished
    # during the scroll, we will skip x new events during the scroll.
    # A naive solution is to implement our own graphql arrayconnection to slice
    # from the last known oid + 1, but the last known oid may not be in the
    # array anymore, so it doesn't work. It's not too bad we skip x events, in
    # reality it should rarely happen.
    rs = find_entities(
        sort_on=None,
        interfaces=interfaces,
        metadata_filter={'states': states},
        text_filter={'text_to_search': args.get('filter', '')},
        intersect=intersect
    )
    catalog = find_catalog('novaideo')
    release_date_index = catalog['release_date']
    return list(release_date_index.sort(
        list(rs.ids), limit=limit, sort_type=STABLE, reverse=True))  #pylint: disable=E1101


def get_all_comments(container, args):
    try:
        after = cursor_to_offset(args.get('after'))
        first = args.get('first')
        if after is None:
            limit = first
        else:
            limit = after + 1 + first

        limit = limit + 1  # retrieve one more so the hasNextPage works
    except Exception:  # FIXME:
        limit = None

    filter_ = args.get('filter', '')
    comments = get_comments(
        container, [], filter_, filter_)
    catalog = find_catalog('novaideo')
    release_date_index = catalog['release_date']
    return list(release_date_index.sort(
        list(comments.ids), limit=limit, sort_type=STABLE, reverse=True))


def get_actions(context, request, args):
    process_id = args.get('process_id', '')
    node_ids = args.get('node_ids', '')
    if not node_ids:
        return [ActionCall(a, context) for a in getAllBusinessAction(
                context, request,
                process_id=process_id,
                process_discriminator='Application')]

    result = []
    for node_id in node_ids:
        result.extend(
            [ActionCall(a, context) for a in getAllBusinessAction(
             context, request,
             process_id=process_id, node_id=node_id,
             process_discriminator='Application')])

    return result


class Node(object):

    @classmethod
    def get_node(cls, id, context, info):  #pylint: disable=W0613,W0622
        oid = int(id)
        return get_obj(oid)


class Root(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, )

    keywords = graphene.List(graphene.String)
    can_add_keywords = graphene.Boolean()


class Action(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, )

    process_id = graphene.String()
    node_id = graphene.String()
    behavior_id = graphene.String()
    title = graphene.String()
    counter = graphene.Int()
    style = graphene.String()
    style_descriminator = graphene.String()
    style_picto = graphene.String()
    style_order = graphene.Int()
    submission_title = graphene.String()

    def resolve_title(self, args, context, info):  # pylint: disable=W0613
        return context.localizer.translate(self.action.title)

    def resolve_submission_title(self, args, context, info):  # pylint: disable=W0613
        submission_title = getattr(self.action, 'submission_title', '')
        return context.localizer.translate(submission_title) if submission_title else submission_title

    def resolve_counter(self, args, context, info):  # pylint: disable=W0613
        action = self.action
        request = get_current_request()
        if hasattr(action, 'get_title'):
            return action.get_title(self.context, request, True)

        return None

    def resolve_process_id(self, args, context, info):  # pylint: disable=W0613
        return self.action.process_id

    def resolve_node_id(self, args, context, info):  # pylint: disable=W0613
        return self.action.node_id

    def resolve_behavior_id(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'behavior_id', self.action.__class__.__name__)

    def resolve_style(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'style', '')

    def resolve_style_descriminator(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'style_descriminator', '')

    def resolve_style_picto(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'style_picto', '')

    def resolve_style_order(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.action, 'style_order', 100)


class File(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, )

    url = graphene.String()
    mimetype = graphene.String()
    is_image = graphene.Boolean()

    def resolve_is_image(self, args, context, info):  #pylint: disable=W0613
        return self.mimetype.startswith('image') or \
            self.mimetype.startswith(
                'application/x-shockwave-flash')


class Person(Node, graphene.ObjectType):

    class Meta(object):
        interfaces = (relay.Node, )

    function = graphene.String()
    description = graphene.String()
    picture = graphene.Field(File)
    first_name = graphene.String()
    last_name = graphene.String()
    title = graphene.String()
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
#    email = graphene.String()
#    email should be visible only by user with Admin or Site Administrator role

    def resolve_contents(self, args, context, info):  # pylint: disable=W0613
        user_ideas = [get_oid(o) for o in getattr(self, 'contents', [])]
        oids = get_entities([Iidea], [], args, info, intersect=user_ideas)
        return ResolverLazyList(oids, Idea)

    def resolve_followed_ideas(self, args, context, info):  # pylint: disable=W0613
        user_ideas = [get_oid(o) for o in getattr(self, 'selections', [])]
        oids = get_entities([Iidea], ['published'], args, info, intersect=user_ideas)
        return ResolverLazyList(oids, Idea)

    def resolve_supported_ideas(self, args, context, info):  # pylint: disable=W0613
        user_ideas = [get_oid(o) for o in getattr(self, 'supports', [])]
        oids = get_entities([Iidea], ['published'], args, info, intersect=user_ideas)
        return ResolverLazyList(oids, Idea)

    def resolve_channels(self, args, context, info):  # pylint: disable=W0613
        return [c for c in getattr(self, 'following_channels', [])
                if not c.is_discuss()]


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


class Comment(Node, graphene.ObjectType):

    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, )

    created_at = graphene.String()
    state = graphene.List(graphene.String)
    text = graphene.String()
    author = graphene.Field(Person)
    attached_files = graphene.List(File)
    urls = graphene.List(Url)
    actions = graphene.List(
        Action,
        process_id=graphene.String(),
        node_ids=graphene.List(graphene.String))
    oid = graphene.String()
    comments = relay.ConnectionField(
        lambda: Comment,
        filter=graphene.String())
    len_comments = graphene.Int()
    root_oid = graphene.String()

    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, SDComment)

    def resolve_created_at(self, args, context, info):
        return self.created_at.isoformat()

    def resolve_text(self, args, context, info):
        return self.comment

    def resolve_urls(self, args, context, info):  # pylint: disable=W0613
        return [Url(**url) for url in getattr(self, 'urls', {}).values()]

    def resolve_oid(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, '__oid__', None)

    def resolve_attached_files(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, 'files', [])

    def resolve_comments(self, args, context, info):  # pylint: disable=W0613
        return ResolverLazyList(
            get_all_comments(self, args),
            Comment)

    def resolve_len_comments(self, args, context, info):
        return self.len_comments

    def resolve_actions(self, args, context, info):  # pylint: disable=W0613
        return get_actions(self, context, args)

    def resolve_root_oid(self, args, context, info):  # pylint: disable=W0613
        return getattr(self.subject, '__oid__', None)
        


class Channel(Node, graphene.ObjectType):

    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, )

    comments = relay.ConnectionField(
        Comment,
        filter=graphene.String())
    
    subject = graphene.Field(lambda: Idea)
    unread_comments = graphene.List(Comment)

    def resolve_comments(self, args, context, info):
        return ResolverLazyList(
            get_all_comments(self, args),
            Comment)

    def resolve_unread_comments(self, args, context, info):
        now = datetime.datetime.now(tz=pytz.UTC)
        return ResolverLazyList(
            self.get_comments_between(
                context.user.get_read_date(self), now), Comment)


class Debatable(graphene.AbstractType):

    channel = graphene.Field(Channel)
    comments = relay.ConnectionField(
        Comment,
        filter=graphene.String())
    len_comments = graphene.Int()

    def resolve_channel(self, args, context, info):
        return self.get_channel(getattr(context, 'user', None))

    def resolve_comments(self, args, context, info):
        channel = self.get_channel(getattr(context, 'user', None))
        return ResolverLazyList(
            get_all_comments(channel, args),
            Comment)

    def resolve_len_comments(self, args, context, info):
        channel = self.get_channel(getattr(context, 'user', None))
        return channel.len_comments if channel else 0


class Idea(Node, Debatable, graphene.ObjectType):

    """Nova-Ideo ideas."""

    class Meta(object):
        interfaces = (relay.Node, )

    created_at = graphene.String()
    state = graphene.List(graphene.String)
    title = graphene.String()
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
    actions = graphene.List(
        Action,
        process_id=graphene.String(),
        node_ids=graphene.List(graphene.String))
    oid = graphene.String()

    @classmethod
    def is_type_of(cls, root, context, info):  # pylint: disable=W0613
        if isinstance(root, cls):
            return True

        return isinstance(root, SDIdea)

    def resolve_created_at(self, args, context, info):
        return self.created_at.isoformat()

    def resolve_presentation_text(self, args, context, info):
        return html_to_text(self.presentation_text(300))

    def resolve_tokens_opposition(self, args, context, info):  # pylint: disable=W0613
        return len(self.tokens_opposition)

    def resolve_tokens_support(self, args, context, info):  # pylint: disable=W0613
        return len(self.tokens_support)

    def resolve_urls(self, args, context, info):  # pylint: disable=W0613
        return [Url(**url) for url in getattr(self, 'urls', {}).values()]

    def resolve_user_token(self, args, context, info):  # pylint: disable=W0613
        user = context.user
        if not user:
            return None
        # @TODO optimization
        if any(t.owner is user for t in self.tokens_support):
            return 'support'

        if any(t.owner is user for t in self.tokens_opposition):
            return 'oppose'

        return None

    def resolve_opinion(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, 'opinion', {}).get('explanation', '')

    def resolve_oid(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, '__oid__', None)

    def resolve_actions(self, args, context, info):  # pylint: disable=W0613
        return get_actions(self, context, args)


class ResolverLazyList(object):

    def __init__(self, origin, object_type, state=None):
        self._origin = origin
        self._state = state or []
        self._origin_iter = None
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


class Query(graphene.ObjectType):

    node = relay.Node.Field()
    ideas = relay.ConnectionField(
        Idea,
        filter=graphene.String()
    )
    account = graphene.Field(Person)
    actions = relay.ConnectionField(
        Action,
        process_id=graphene.String(),
        node_ids=graphene.List(graphene.String),
        context=graphene.String()
    )
    root = graphene.Field(Root)

    def resolve_ideas(self, args, context, info):  # pylint: disable=W0613
        oids = get_entities([Iidea], ['published'], args, info)
        return ResolverLazyList(oids, Idea)

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
