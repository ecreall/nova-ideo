import graphene

from .processes.abstract_process import Select, Deselect, AddReaction
from .processes.idea_management import (
    CreateIdea, CreateAndPublishIdea, DeleteIdea,
    Support, Oppose, WithdrawToken, Publish, EditIdea)
from .processes.comment_management import (
    CommentObject, MarkCommentsAsRead, DeleteComment,
    Pin, Unpin, Edit, AddPrivateChannel)
from .processes.user_management import Registration, ConfirmRegistration

class Mutations(graphene.ObjectType):
    # abstract process
    select = Select.Field()
    deselect = Deselect.Field()
    add_reaction = AddReaction.Field()
    # idea management process
    create_idea = CreateIdea.Field()
    edit_idea = EditIdea.Field()
    create_and_publish = CreateAndPublishIdea.Field()
    publish_idea = Publish.Field()
    delete_idea = DeleteIdea.Field()
    support_idea = Support.Field()
    oppose_idea = Oppose.Field()
    withdraw_token_idea = WithdrawToken.Field()
    # comment management process
    add_private_channel = AddPrivateChannel.Field()
    comment_object = CommentObject.Field()
    mark_as_read = MarkCommentsAsRead.Field()
    delete_comment = DeleteComment.Field()
    pin_comment = Pin.Field()
    unpin_comment = Unpin.Field()
    edit_comment = Edit.Field()
    # user management
    registration = Registration.Field()
    confirm_registration = ConfirmRegistration.Field()