/* eslint-disable import/prefer-default-export, import/no-extraneous-dependencies */
import StarBorderIcon from '@material-ui/icons/StarBorder';
import StarIcon from '@material-ui/icons/Star';
import HistoryIcon from '@material-ui/icons/History';
import ArchiveIcon from '@material-ui/icons/Archive';
import UnarchiveIcon from '@material-ui/icons/Unarchive';
import ReportIcon from '@material-ui/icons/Report';
import ReplyIcon from '@material-ui/icons/Reply';
import ModeEditIcon from '@material-ui/icons/Edit';
import DeleteIcon from '@material-ui/icons/Delete';
import PaletteIcon from '@material-ui/icons/Palette';
import SettingsIcon from '@material-ui/icons/Settings';
import WorkIcon from '@material-ui/icons/Work';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import QuestionAnswerIcon from '@material-ui/icons/QuestionAnswer';

import { iconAdapter } from './utils/globalFunctions';

export const PROCESSES = {
  ideamanagement: {
    id: 'ideamanagement',
    nodes: {
      create: {
        nodeId: 'creat',
        submission: 'processes.ideamanagement.create.submission'
      },
      createAndPublish: {
        nodeId: 'creatandpublish',
        submission: 'processes.ideamanagement.createAndPublish.submission',
        submissionModeration: 'processes.ideamanagement.createAndPublish.submissionModeration'
      },
      comment: {
        nodeId: 'comment',
        title: 'processes.ideamanagement.comment.title',
        description: 'processes.ideamanagement.comment.description',
        color: '#d72b3f'
      },
      commentAnonymous: {
        nodeId: 'comment',
        behaviorId: 'comment_anonymous',
        title: 'processes.ideamanagement.comment.title',
        description: 'processes.ideamanagement.comment.description',
        color: '#d72b3f'
      },
      support: {
        nodeId: 'support',
        title: 'processes.ideamanagement.support.title',
        description: 'processes.ideamanagement.support.description'
      },
      oppose: {
        nodeId: 'oppose',
        title: 'processes.ideamanagement.oppose.title',
        description: 'processes.ideamanagement.oppose.description'
      },
      withdrawToken: {
        nodeId: 'withdraw_token',
        title: 'processes.ideamanagement.withdrawToken.title',
        description: 'processes.ideamanagement.withdrawToken.description'
      },
      delete: {
        nodeId: 'delidea',
        title: 'processes.ideamanagement.delete.title',
        description: 'processes.ideamanagement.delete.description',
        submission: 'processes.ideamanagement.delete.submission',
        confirmation: 'processes.ideamanagement.delete.confirmation'
      },
      edit: {
        nodeId: 'edit',
        title: 'processes.ideamanagement.edit.title',
        description: 'processes.ideamanagement.edit.description',
        submission: 'processes.ideamanagement.edit.submission',
        confirmation: 'processes.ideamanagement.edit.confirmation'
      },
      publish: {
        nodeId: 'publish',
        title: 'processes.ideamanagement.publish.title',
        description: 'processes.ideamanagement.publish.description',
        submission: 'processes.ideamanagement.publish.submission',
        confirmation: 'processes.ideamanagement.publish.confirmation'
      },
      abandon: {
        nodeId: 'abandon',
        title: 'processes.ideamanagement.abandon.title',
        description: 'processes.ideamanagement.abandon.description',
        submission: 'processes.ideamanagement.abandon.submission',
        confirmation: 'processes.ideamanagement.abandon.confirmation',
        icon: ArchiveIcon
      },
      archive: {
        nodeId: 'moderationarchive',
        title: 'processes.ideamanagement.archive.title',
        description: 'processes.ideamanagement.archive.description',
        submission: 'processes.ideamanagement.archive.submission',
        confirmation: 'processes.ideamanagement.archive.confirmation',
        icon: ArchiveIcon
      },
      recuperate: {
        nodeId: 'recuperate',
        title: 'processes.ideamanagement.recuperate.title',
        description: 'processes.ideamanagement.recuperate.description',
        submission: 'processes.ideamanagement.recuperate.submission',
        confirmation: 'processes.ideamanagement.recuperate.confirmation',
        icon: UnarchiveIcon
      },
      makeItsOpinion: {
        nodeId: 'makeitsopinion',
        title: 'processes.ideamanagement.makeItsOpinion.title',
        description: 'processes.ideamanagement.makeItsOpinion.description',
        icon: iconAdapter('mdi-set mdi-clipboard-check')
      },
      share: {
        nodeId: 'present',
        title: 'processes.ideamanagement.present.title',
        description: 'processes.ideamanagement.present.description',
        icon: iconAdapter('mdi-set mdi-share')
      },
      shareAnonymous: {
        nodeId: 'present',
        behaviorId: 'present_anonymous',
        title: 'processes.ideamanagement.present.title',
        description: 'processes.ideamanagement.present.description',
        icon: iconAdapter('mdi-set mdi-share')
      },
      submit: {
        nodeId: 'submit',
        title: 'processes.ideamanagement.submit.title',
        description: 'processes.ideamanagement.submit.description',
        submission: 'processes.ideamanagement.submit.submission',
        confirmation: 'processes.ideamanagement.submit.confirmation',
        icon: iconAdapter('mdi-set mdi-send')
      },
      moderationArchive: {
        nodeId: 'archive',
        title: 'processes.ideamanagement.moderationArchive.title',
        description: 'processes.ideamanagement.moderationArchive.description',
        submission: 'processes.ideamanagement.moderationArchive.submission',
        confirmation: 'processes.ideamanagement.moderationArchive.confirmation',
        icon: ArchiveIcon
      },
      moderationPublish: {
        nodeId: 'publish_moderation',
        title: 'processes.ideamanagement.moderationPublish.title',
        description: 'processes.ideamanagement.moderationPublish.description',
        submission: 'processes.ideamanagement.moderationPublish.submission',
        confirmation: 'processes.ideamanagement.moderationPublish.confirmation',
        icon: iconAdapter('mdi-set mdi-earth')
      }
    }
  },
  usermanagement: {
    id: 'usermanagement',
    nodes: {
      login: {
        nodeId: 'login',
        title: 'processes.usermanagement.login.title',
        icon: iconAdapter('mdi-set mdi-login-variant')
      },
      logout: {
        nodeId: 'logout',
        title: 'processes.usermanagement.logout.title',
        icon: iconAdapter('mdi-set mdi-logout-variant')
      },
      discuss: {
        nodeId: 'discuss',
        title: 'processes.usermanagement.discuss.title',
        description: 'processes.usermanagement.discuss.description',
        color: '#d72b3f'
      },
      generalDiscuss: {
        nodeId: 'general_discuss',
        title: 'processes.usermanagement.generalDiscuss.title'
      },
      edit: {
        nodeId: 'edit',
        title: 'processes.usermanagement.edit.title',
        description: 'processes.usermanagement.edit.description'
      },
      assignRoles: {
        nodeId: 'assign_roles',
        title: 'processes.usermanagement.assignRoles.title',
        description: 'processes.usermanagement.assignRoles.description'
      },
      getApiToken: {
        nodeId: 'get_api_token',
        title: 'processes.usermanagement.getApiToken.title',
        description: 'processes.usermanagement.getApiToken.description'
      },
      editPassword: {
        nodeId: 'edit_password',
        title: 'processes.usermanagement.editPassword.title',
        description: 'processes.usermanagement.editPassword.description'
      },
      editPreferences: {
        nodeId: 'edit_preferences',
        title: 'processes.usermanagement.editPreferences.title',
        description: 'processes.usermanagement.editPreferences.description',
        icon: PaletteIcon
      },
      see: {
        nodeId: 'see',
        title: 'processes.usermanagement.see.title',
        description: 'processes.usermanagement.see.description'
      },
      deactivate: {
        nodeId: 'deactivate',
        title: 'processes.usermanagement.deactivate.title',
        description: 'processes.usermanagement.deactivate.description',
        submission: 'processes.usermanagement.deactivate.submission',
        confirmation: 'processes.usermanagement.deactivate.confirmation',
        icon: iconAdapter('mdi-set mdi-account-off')
      },
      activate: {
        nodeId: 'activate',
        title: 'processes.usermanagement.activate.title',
        description: 'processes.usermanagement.activate.description',
        submission: 'processes.usermanagement.activate.submission',
        confirmation: 'processes.usermanagement.activate.confirmation',
        icon: iconAdapter('mdi-set mdi-account-key')
      }
    }
  },
  registrationmanagement: {
    id: 'registrationmanagement',
    nodes: {
      registration: {
        nodeId: 'registration',
        title: 'processes.registrationmanagement.registration.title',
        description: 'processes.registrationmanagement.registration.title',
        icon: iconAdapter('mdi-set mdi-account-plus')
      }
    }
  },
  novaideoabstractprocess: {
    id: 'novaideoabstractprocess',
    nodes: {
      select: {
        nodeId: 'select',
        title: 'processes.novaideoabstractprocess.select.title',
        description: 'processes.novaideoabstractprocess.select.title'
      },
      selectAnonymous: {
        nodeId: 'select',
        behaviorId: 'select_anonymous',
        title: 'processes.novaideoabstractprocess.select.title',
        description: 'processes.novaideoabstractprocess.select.title'
      },
      deselect: {
        nodeId: 'deselect',
        title: 'processes.novaideoabstractprocess.deselect.title',
        description: 'processes.novaideoabstractprocess.deselect.title',
        color: '#2ea664'
      },
      addreaction: {
        nodeId: 'addreaction',
        title: 'processes.novaideoabstractprocess.addreaction.title',
        description: 'processes.novaideoabstractprocess.addreaction.title'
      },
      addDeadline: {
        nodeId: 'adddeadline',
        title: 'processes.novaideoabstractprocess.adddeadline.title',
        description: 'processes.novaideoabstractprocess.adddeadline.title'
      },
      editDeadline: {
        nodeId: 'editdeadline',
        title: 'processes.novaideoabstractprocess.editdeadline.title',
        description: 'processes.novaideoabstractprocess.editdeadline.title'
      }
    }
  },
  commentmanagement: {
    id: 'commentmanagement',
    nodes: {
      delete: {
        nodeId: 'remove',
        title: 'processes.commentmanagement.delete.title',
        description: 'processes.commentmanagement.delete.description',
        submission: 'processes.commentmanagement.delete.submission',
        confirmation: 'processes.commentmanagement.delete.confirmation'
      },
      transformtoidea: {
        nodeId: 'transformtoidea',
        title: 'processes.commentmanagement.transformtoidea.title',
        description: 'processes.commentmanagement.transformtoidea.description'
      },
      pin: {
        nodeId: 'pin',
        title: 'processes.commentmanagement.pin.title',
        description: 'processes.commentmanagement.pin.description',
        submission: 'processes.commentmanagement.pin.submission',
        confirmation: 'processes.commentmanagement.pin.confirmation'
      },
      unpin: {
        nodeId: 'unpin',
        title: 'processes.commentmanagement.unpin.title',
        description: 'processes.commentmanagement.unpin.description',
        submission: 'processes.commentmanagement.unpin.submission',
        confirmation: 'processes.commentmanagement.unpin.confirmation'
      },
      respond: {
        nodeId: 'respond',
        title: 'processes.commentmanagement.respond.title',
        description: 'processes.commentmanagement.respond.description'
      },
      edit: {
        nodeId: 'edit',
        title: 'processes.commentmanagement.edit.title',
        description: 'processes.commentmanagement.edit.description',
        submission: 'processes.commentmanagement.edit.submission'
      }
    }
  }
};

export const ACTIONS = {
  communication: 'communication',
  primary: 'primary',
  danger: 'danger',
  info: 'info',
  success: 'success',
  warning: 'warning',
  secondary: 'secondary',
  entity: 'entity',
  global: 'global',
  other: 'other',
  menu: 'menu',
  mainMenu: 'main-menu',
  site: 'site',
  parametersMenu: 'parameters-menu'
};

export const STATE = {
  idea: {
    private: 'to work',
    published: 'published',
    submittedSupport: 'submitted_support',
    toStudy: 'to_study',
    favorable: 'favorable',
    unfavorable: 'unfavorable',
    examined: 'examined',
    submitted: 'submitted',
    archived: 'archived'
  }
};

export const STATE_LABEL = {
  idea: {
    [STATE.idea.private]: { title: 'states.idea.private', icon: iconAdapter('mdi-set mdi-lock') },
    [STATE.idea.published]: { title: 'states.idea.published', icon: iconAdapter('mdi-set mdi-earth') },
    [STATE.idea.submittedSupport]: {
      title: 'states.idea.submittedSupport',
      icon: iconAdapter('mdi-set mdi-arrow-up-drop-circle')
    },
    [STATE.idea.toStudy]: { title: 'states.idea.toStudy', icon: iconAdapter('mdi-set mdi-checkbox-blank-circle') },
    [STATE.idea.favorable]: { title: 'states.idea.favorable', icon: iconAdapter('mdi-set mdi-checkbox-blank-circle') },
    [STATE.idea.unfavorable]: { title: 'states.idea.unfavorable', icon: iconAdapter('mdi-set mdi-checkbox-blank-circle') },
    [STATE.idea.examined]: { title: 'states.idea.examined', icon: iconAdapter('mdi-set mdi-checkbox-blank-circle') },
    [STATE.idea.submitted]: { title: 'states.idea.submitted', icon: iconAdapter('mdi-set mdi-send') },
    [STATE.idea.archived]: { title: 'states.idea.archived', icon: iconAdapter('mdi-set mdi-package-down') }
  }
};

export const COMMENTS_ACTIONS = ['comment', 'discuss', 'general_discuss'];

export const ICONS_MAPPING = {
  'ion-chatbubble': iconAdapter('mdi-set mdi-comment-outline'),
  'glyphicon glyphicon-share-alt': iconAdapter('mdi-set mdi-share'),
  'glyphicon glyphicon-star-empty': StarBorderIcon,
  'glyphicon glyphicon-star': StarIcon,
  'glyphicon glyphicon-time': HistoryIcon,
  'md md-sms-failed': ReportIcon,
  'ion-chatbubbles': ReplyIcon,
  'glyphicon glyphicon-pencil': ModeEditIcon,
  'glyphicon glyphicon-settings': SettingsIcon,
  'glyphicon glyphicon-trash': DeleteIcon,
  'icon md md-live-help': QuestionAnswerIcon,
  'typcn typcn-pin': iconAdapter('mdi-set mdi-pin'),
  'typcn typcn-pin-outline': iconAdapter('mdi-set mdi-pin-off'),
  'icon novaideo-icon icon-idea': iconAdapter('mdi-set mdi-lightbulb'),
  'glyphicon glyphicon-share': iconAdapter('mdi-set mdi-earth'),
  'glyphicon glyphicon-tower': WorkIcon,
  'glyphicon glyphicon-profile': AccountCircleIcon
};

export const ENTITIES_ICONS = {
  Idea: iconAdapter('mdi-set mdi-lightbulb'),
  default: iconAdapter('mdi-set mdi-pound')
};