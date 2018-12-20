import graphene

from .processes.abstract_process import Select, Deselect, AddReaction
from .processes.idea_management import (
    CreateIdea, CreateAndPublishIdea, DeleteIdea,
    Support, Oppose, WithdrawToken, Publish, EditIdea,
    MakeItsOpinion, Abandon, Archive, Recuperate, Share)
from .processes.comment_management import (
    CommentObject, MarkCommentsAsRead, DeleteComment,
    Pin, Unpin, Edit, AddPrivateChannel)
from .processes.user_management import (
    Registration, ConfirmRegistration,
    EditProfile, EditPassword,
    EditApiToken, AssignRoles,
    Activate, Deactivate, ResetPassword,
    ConfirmResetPassword, MarkAlertsAsRead)
from .processes.admin_process import EditDeadline, AddDeadline


class Mutations(graphene.ObjectType):
    # admin process
    add_deadline = AddDeadline.Field()
    edit_deadline = EditDeadline.Field()
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
    make_its_opinion = MakeItsOpinion.Field()
    abandon_idea = Abandon.Field()
    recuperate_idea = Recuperate.Field()
    archive_idea = Archive.Field()
    share = Share.Field()
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
    edit_profile = EditProfile.Field()
    edit_password = EditPassword.Field()
    edit_api_token = EditApiToken.Field()
    assign_roles = AssignRoles.Field()
    activate = Activate.Field()
    deactivate = Deactivate.Field()
    reset_password = ResetPassword.Field()
    confirm_reset_password = ConfirmResetPassword.Field()
    mark_alerts_as_read = MarkAlertsAsRead.Field()