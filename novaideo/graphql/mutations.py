import graphene

from .processes.abstract_process import Select, Deselect
from .processes.idea_management import CreateIdea, CreateAndPublishIdea, DeleteIdea, Support, Oppose, WithdrawToken
from .processes.comment_management import CommentObject, MarkCommentsAsRead, DeleteComment, Pin, Unpin

class Mutations(graphene.ObjectType):
    # abstract process
    select = Select.Field()
    deselect = Deselect.Field()
    # idea management process
    create_idea = CreateIdea.Field()
    create_and_publish = CreateAndPublishIdea.Field()
    delete_idea = DeleteIdea.Field()
    support_idea = Support.Field()
    oppose_idea = Oppose.Field()
    withdraw_token_idea = WithdrawToken.Field()
    # comment management process
    comment_object = CommentObject.Field()
    mark_comments_as_read = MarkCommentsAsRead.Field()
    delete_comment = DeleteComment.Field()
    pin_comment = Pin.Field()
    unpin_comment = Unpin.Field()