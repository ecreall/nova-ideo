# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from zope.interface import invariant

from pontus.schema import omit, select, Schema
from pontus.widget import (
    SequenceWidget, SimpleMappingWidget,
    CheckboxChoiceWidget, Select2Widget,
    RichTextWidget)
from pontus.file import ObjectData, File

from novaideo.content.processes.proposal_management import WORK_MODES
from novaideo import _
from novaideo.mail import DEFAULT_SITE_MAILS
from novaideo.core_schema import ContactSchema
from novaideo import core
from novaideo.content import get_file_widget


@colander.deferred
def modes_choice(node, kw):
    request = node.bindings['request']
    localizer = request.localizer
    modes = list(WORK_MODES.items())
    modes = sorted(modes, key=lambda e: e[1].order)
    values = [(key, localizer.translate(value.title)) for key, value in modes]
    return CheckboxChoiceWidget(values=values, multiple=True)


@colander.deferred
def content_types_choices(node, kw):
    content_to_examine = ['idea', 'proposal']
    request = node.bindings['request']
    localizer = request.localizer
    values = [(key, localizer.translate(
              getattr(c, 'type_title', c.__class__.__name__)))
              for key, c in list(core.SEARCHABLE_CONTENTS.items())
              if key in content_to_examine]
    return CheckboxChoiceWidget(values=sorted(values), multiple=True)


class WorkParamsConfigurationSchema(Schema):
    """Schema for site configuration."""

    is_idea_box = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Is a suggestion box'),
        description=_('In a suggestion box, only the ideas are managed.'),
        title='',
        missing=False
    )

    content_to_moderate = colander.SchemaNode(
        colander.Set(),
        widget=content_types_choices,
        title=_('Contents to be moderated'),
        description=_('Contents can be moderated.'),
        missing=[]
    )

    content_to_support = colander.SchemaNode(
        colander.Set(),
        widget=content_types_choices,
        title=_('Contents to be supported'),
        description=_('Contents can be supported by users.'),
        missing=[]
    )

    content_to_examine = colander.SchemaNode(
        colander.Set(),
        widget=content_types_choices,
        title=_('Contents to be examined'),
        description=_('Contents must be examined by a review committee.'),
        missing=[]
    )

    proposal_template = colander.SchemaNode(
        ObjectData(File),
        widget=get_file_widget(file_extensions=['html']),
        title=_('Proposal template'),
        missing=None,
        description=_("Only HTML files are supported."),
        )

    work_modes = colander.SchemaNode(
        colander.Set(),
        title=_('Work modes'),
        description=_('Work modes of the working group (for proposals).'),
        widget=modes_choice,
        default=[],
    )

    nonproductive_cycle_nb = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(1, 10),
        title=_('Number of non-productive cycles'),
        description=_('The number of non-productive improvement cycles before the closure of the working group.'),
        default=3,
        )


class UserParamsConfigurationSchema(Schema):

    only_invitation = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('By invitation only'),
        description=_('Users can register by invitation only.'),
        title='',
        missing=False
    )

    moderate_registration = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Moderate user registration'),
        description=_('Moderate user registration.'),
        title='',
        missing=False
    )

    trusted_emails = colander.SchemaNode(
        colander.Set(),
        widget=Select2Widget(
            values=[],
            create=True,
            multiple=True),
        title=_('Trusted email addresses'),
        description=_("To add trusted email addresses, you need to tap the « Enter »"
                      " key after each email address or to separate them with commas."),
        missing=[]
        )

    only_for_members = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Accessible by Members only'),
        description=_('Contents can be displayed by Member sonly.'),
        title='',
        missing=False
    )

    # participants_mini = colander.SchemaNode(
    #     colander.Integer(),
    #     title=_('Minimum number of participants for a working group'),
    #     default=3,
    #     )

    participants_maxi = colander.SchemaNode(
        colander.Integer(),
        title=_('Maximum number of Participants per Working Group'),
        default=12,
        )

    participations_maxi = colander.SchemaNode(
        colander.Integer(),
        title=_('Maximum number of Working Groups per Member'),
        default=5,
        )

    tokens_mini = colander.SchemaNode(
        colander.Integer(),
        title=_('Minimum number of evaluation Tokens allocated to a Member'),
        default=7,
        )


class UserInterfaceConfigurationSchema(Schema):

    picture = colander.SchemaNode(
        ObjectData(File),
        widget=get_file_widget(file_extensions=['png', 'jpg', 'svg']),
        title=_('Logo'),
        missing=None,
        description=_("Only PNG and SVG files are supported."),
        )

    favicon = colander.SchemaNode(
        ObjectData(File),
        widget=get_file_widget(file_extensions=['ico']),
        title=_('Favicon'),
        missing=None,
        description=_("Only ICO files are supported."),
        )

    theme = colander.SchemaNode(
        ObjectData(File),
        widget=get_file_widget(file_extensions=['css']),
        title=_('Theme'),
        missing=None,
        description=_("Only CSS files are supported."),
        )

    social_share = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Activate the sharing on social networks'),
        title='',
        missing=False
        )


class HomepageConfigurationSchema(Schema):

    homepage_picture = colander.SchemaNode(
        ObjectData(File),
        widget=get_file_widget(file_extensions=['png', 'jpg', 'svg']),
        title=_('Picture of the homepage'),
        missing=None,
        description=_("Only PNG and SVG files are supported."),
        )

    homepage_text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_("Text"),
        missing=''
        )


class MailTemplate(Schema):

    mail_id = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        title=_('Mail id'),
        )

    title = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextInputWidget(template='readonly/textinput'),
        title=_('Title'),
        missing=""
        )

    subject = colander.SchemaNode(
        colander.String(),
        title=_('Subject'),
        )

    template = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        title=_("Template")
        )


@colander.deferred
def templates_widget(node, kw):
    len_templates = len(DEFAULT_SITE_MAILS)
    return SequenceWidget(min_len=len_templates, max_len=len_templates)


@colander.deferred
def templates_default(node, kw):
    request = node.bindings['request']
    localizer = request.localizer
    values = []
    for temp_id in DEFAULT_SITE_MAILS:
        template = DEFAULT_SITE_MAILS[temp_id].copy()
        template['mail_id'] = temp_id
        template['title'] = localizer.translate(template['title'])
        values.append(template)

    values = sorted(values, key=lambda e: e['mail_id'])
    return values


class MailTemplatesConfigurationSchema(Schema):

    mail_templates = colander.SchemaNode(
        colander.Sequence(),
        omit(select(MailTemplate(name='template',
                                 title=_('E-mail template'),
                                 widget=SimpleMappingWidget(
                                         css_class="object-well default-well mail-template-well mail-template-block")),
                        ['mail_id', 'title', 'subject', 'template']),
                    ['_csrf_token_']),
        widget=templates_widget,
        default=templates_default,
        missing=templates_default,
        title=_('E-mail templates'),
        )


@colander.deferred
def keywords_choice(node, kw):
    context = node.bindings['context']
    values = [(i, i) for i in sorted(getattr(context, 'keywords', []))]
    return Select2Widget(values=values,
                         create=True,
                         multiple=True)


class KeywordsConfSchema(Schema):

    keywords = colander.SchemaNode(
        colander.Set(),
        widget=keywords_choice,
        title='Keywords',
        description=_("To add keywords, you need to tap the « Enter »"
                      " key after each keyword or separate them with commas."),
        missing=[]
        )

    can_add_keywords = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Authorize the addition of keywords'),
        title='',
        default=True,
        missing=True
    )

    @invariant
    def contact_invariant(self, appstruct):
        can_add_keywords = appstruct.get('can_add_keywords', 'false')
        can_add_keywords = False if can_add_keywords == 'false' else True
        keywords = appstruct.get('keywords', colander.null)
        if not can_add_keywords and keywords is colander.null:
            raise colander.Invalid(
                self, _('You must enter at least one keyword.'))


class OtherSchema(Schema):

    title = colander.SchemaNode(
        colander.String(),
        title=_('Title'),
        description=_("The title of the application"),
        missing=""
        )

    contacts = colander.SchemaNode(
        colander.Sequence(),
        omit(select(ContactSchema(name='contact',
                                  widget=SimpleMappingWidget(
                                  css_class='contact-well object-well default-well')),
                    ['title', 'address', 'phone', 'surtax', 'email', 'website', 'fax']),
            ['_csrf_token_']),
        widget=SequenceWidget(
            add_subitem_text_template=_('Add a new contact')),
        title='Contacts',
        oid='contacts'
        )

    analytics = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        title=_('Analytics'),
        missing=''
        )


class NotificationConfigurationSchema(Schema):
    """Schema for site configuration."""

    activate_push_notification = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Activate the push notifications on the browser'),
        title='',
        missing=False
    )

    app_id = colander.SchemaNode(
        colander.String(),
        title=_('Application id'),
        missing=""
        )

    app_key = colander.SchemaNode(
        colander.String(),
        title=_('REST API Key'),
        missing=""
        )
