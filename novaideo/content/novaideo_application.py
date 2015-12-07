# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import colander
import datetime
from zope.interface import implementer
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer
from substanced.property import PropertySheet

from dace.objectofcollaboration.application import Application
from dace.descriptors import CompositeMultipleProperty
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import (
    SequenceWidget,
    SimpleMappingWidget)
from pontus.file import ObjectData as ObjectDataOrigine
from pontus.schema import omit, select

from novaideo import _, DEFAULT_FILES
from novaideo.core import FileEntity
from .organization import OrganizationSchema, Organization
from .interface import INovaIdeoApplication
from .invitation import InvitationSchema, Invitation
from novaideo.content.keyword import Keyword
from novaideo.content.processes.proposal_management import WORK_MODES
from novaideo.mail import DEFAULT_SITE_MAILS
from novaideo.views.widget import SimpleMappingtWidget
from novaideo.content.site_configuration import (
    WorkParamsConfigurationSchema,
    MailTemplatesConfigurationSchema,
    UserParamsConfigurationSchema,
    KeywordsConfSchema,
    OtherSchema,
)


DEFAULT_TITLES = [_('Mr'), _('Madam'), _('Miss')]

DEFAULT_COMMENT_INTENTIONS = [
    _('Changing an idea'),
    _('Propose improvements'),
    _('Reformulate'),
    _('Generalize'),
    _('Expand'),
    _('Ask a question'),
    _('Review'),
    _('Irony'),
    _('Use humor')
]

DEFAULT_CORRELATION_INTENTIONS = [_('Irony'), _('Humor'), _('Remark')]

DEFAULT_IDEA_INTENTIONS = [_('Improvement'), _('Humor'), _('Irony')]

DEFAULT_AMENDMENT_INTENTIONS = [_('Irony'), _('Humor'), _('Remark')]


def context_is_a_root(context, request):
    return request.registry.content.istype(context, 'Root')


class ObjectData(ObjectDataOrigine):

    def clean_cstruct(self, node, cstruct):
        result, appstruct, hasevalue = super(ObjectData, self)\
            .clean_cstruct(node, cstruct)

        if 'work_conf' in result:
            work_conf = result.pop('work_conf')
            result.update(work_conf)

        if 'user_conf' in result:
            user_conf = result.pop('user_conf')
            result.update(user_conf)

        if 'mail_conf' in result:
            mail_conf = result.pop('mail_conf')
            templates = mail_conf['mail_templates']
            for template in templates:
                mail_id = template['mail_id']
                if mail_id in DEFAULT_SITE_MAILS:
                    template['title'] = DEFAULT_SITE_MAILS[mail_id]['title']

            result.update(mail_conf)

        if 'keywords_conf' in result:
            keywords_conf = result.pop('keywords_conf')
            result.update(keywords_conf)

        if 'other_conf' in result:
            other_conf = result.pop('other_conf')
            result.update(other_conf)

        return result, appstruct, hasevalue


@colander.deferred
def invitations_choice(node, kw):
    context = node.bindings['context']
    len_invitations = len(context.invitations)
    if len_invitations == 0:
        len_invitations = -1

    return SequenceWidget(min_len=len_invitations,
                          max_len=len_invitations)


@colander.deferred
def organizations_choice(node, kw):
    context = node.bindings['context']
    len_organizations = len(context.organizations)
    if len_organizations == 0:
        len_organizations = -1

    return SequenceWidget(min_len=len_organizations,
                          max_len=len_organizations)


class NovaIdeoApplicationSchema(VisualisableElementSchema):
    """Schema for Nova-Ideo configuration"""

    typ_factory = ObjectData

    name = NameSchemaNode(
        editing=context_is_a_root,
        )

    invitations = colander.SchemaNode(
        colander.Sequence(),
        omit(InvitationSchema(factory=Invitation,
                               editable=True,
                               name=_('Invitations'),
                               widget=SimpleMappingWidget(css_class='object-well default-well')),
            ['_csrf_token_']),
        widget=invitations_choice,
        title=_('List of invitation'),
        )

    organizations = colander.SchemaNode(
        colander.Sequence(),
        omit(OrganizationSchema(factory=Organization,
                editable=True,
                name=_('Organization'),
                widget=SimpleMappingWidget(css_class='object-well default-well'),
                omit=['managers']),
            ['_csrf_token_']),
        widget=organizations_choice,
        title=_('Organizations'),
        )

    work_conf = omit(WorkParamsConfigurationSchema(
                                widget=SimpleMappingtWidget(
                                mapping_css_class='controled-form'
                                                  ' object-well default-well hide-bloc',
                                ajax=True,
                                activator_icon="glyphicon glyphicon-filter",
                                activator_title=_('Set up work parameters'))),
                        ["_csrf_token_"])

    mail_conf = omit(MailTemplatesConfigurationSchema(
                                widget=SimpleMappingtWidget(
                                mapping_css_class='controled-form'
                                                  ' object-well default-well hide-bloc',
                                ajax=True,
                                activator_icon="glyphicon glyphicon-envelope",
                                activator_title=_('Edit mail templates'))),
                        ["_csrf_token_"])

    user_conf = omit(UserParamsConfigurationSchema(
                                widget=SimpleMappingtWidget(
                                mapping_css_class='controled-form'
                                                  ' object-well default-well hide-bloc',
                                ajax=True,
                                activator_icon="glyphicon glyphicon-user",
                                activator_title=_('Configure user parameters'))),
                        ["_csrf_token_"])
    keywords_conf = omit(KeywordsConfSchema(
                                widget=SimpleMappingtWidget(
                                mapping_css_class='controled-form'
                                                  ' object-well default-well hide-bloc',
                                ajax=True,
                                activator_icon="glyphicon glyphicon-tags",
                                activator_title=_('Configure keywords'))),
                        ["_csrf_token_"])

    other_conf = omit(OtherSchema(
                                widget=SimpleMappingtWidget(
                                mapping_css_class='controled-form'
                                                  ' object-well default-well hide-bloc',
                                ajax=True,
                                activator_icon="glyphicon glyphicon-plus",
                                activator_title=_('Other'))),
                        ["_csrf_token_"])



class NovaIdeoApplicationPropertySheet(PropertySheet):
    schema = select(NovaIdeoApplicationSchema(), ['title',
                                                  'work_modes',
                                                  'tokens_mini'])


@content(
    'Root',
    icon='glyphicon glyphicon-home',
    propertysheets = (
        ('Basic', NovaIdeoApplicationPropertySheet),
        ),
    after_create='after_create',
    )
@implementer(INovaIdeoApplication)
class NovaIdeoApplication(VisualisableElement, Application):
    """Nova-Ideo class (Root)"""

    name = renamer()
    preregistrations = CompositeMultipleProperty('preregistrations')
    working_groups = CompositeMultipleProperty('working_groups')
    proposals = CompositeMultipleProperty('proposals')
    organizations = CompositeMultipleProperty('organizations')
    invitations = CompositeMultipleProperty('invitations')
    ideas = CompositeMultipleProperty('ideas')
    correlations = CompositeMultipleProperty('correlations')
    files = CompositeMultipleProperty('files')

    def __init__(self, **kwargs):
        super(NovaIdeoApplication, self).__init__(**kwargs)
        self.keywords = PersistentList()
        self.initialization()

    @property
    def mail_conf(self):
        return self.get_data(omit(MailTemplatesConfigurationSchema(),
                                 '_csrf_token_'))

    @property
    def work_conf(self):
        result = self.get_data(omit(WorkParamsConfigurationSchema(),
                                  '_csrf_token_'))
        return result

    @property
    def user_conf(self):
        return self.get_data(omit(UserParamsConfigurationSchema(),
                                  '_csrf_token_'))

    @property
    def keywords_conf(self):
        return self.get_data(omit(KeywordsConfSchema(),
                                  '_csrf_token_'))

    @property
    def other_conf(self):
        return self.get_data(omit(OtherSchema(),
                                  '_csrf_token_'))

    def initialization(self):
        self.reset_default_values()
        self.deadlines = PersistentList([datetime.datetime.now(tz=pytz.UTC)])
        self.work_modes = list(WORK_MODES.keys())

    def reset_default_values(self):
        self.participants_mini = 3
        self.participants_maxi = 12
        self.participations_maxi = 5
        self.tokens_mini = 7
        self.titles = DEFAULT_TITLES
        self.comment_intentions = DEFAULT_COMMENT_INTENTIONS
        self.correlation_intentions = DEFAULT_CORRELATION_INTENTIONS
        self.idea_intentions = DEFAULT_IDEA_INTENTIONS
        self.amendment_intentions = DEFAULT_AMENDMENT_INTENTIONS

    def init_files(self):
        for information in DEFAULT_FILES:
            if not self.get(information['name'], None):
                info_file = FileEntity(title=information['title'])
                info_file.text = information['content']
                info_file.__name__ = information['name']
                self.addtoproperty('files', info_file)

    def get_mail_template(self, id):
        for mail in getattr(self, 'mail_templates', {}):
            if mail.get('mail_id', None) == id:
                return mail

        template = DEFAULT_SITE_MAILS.get(id, None)
        if template:
            template = template.copy()
            template['mail_id'] = id

        return template

    def get_site_sender(self):
        registry = get_current_registry()
        default_sender = registry.settings['novaideo.admin_email']
        return getattr(self, 'site_sender', default_sender)

    def get_work_modes(self):
        modes = getattr(self, 'work_modes', [])
        modes = {m: WORK_MODES[m] for m in modes if m in WORK_MODES}
        if modes:
            return modes

        return WORK_MODES

    def get_default_work_mode(self):
        modes = list(self.get_work_modes().values())
        modes = sorted(modes, key=lambda e: e.order)
        return modes[0]

    def merge_keywords(self, newkeywords):
        self.keywords.extend([kw for kw in newkeywords
                               if kw not in self.keywords])
