/* eslint-disable import/prefer-default-export, import/no-extraneous-dependencies */
import StarBorderIcon from '@material-ui/icons/StarBorder';
import StarIcon from '@material-ui/icons/Star';
import HistoryIcon from '@material-ui/icons/History';
import ReportIcon from '@material-ui/icons/Report';
import ReplyIcon from '@material-ui/icons/Reply';
import ModeEditIcon from '@material-ui/icons/ModeEdit';
import DeleteIcon from '@material-ui/icons/Delete';
import SettingsIcon from '@material-ui/icons/Settings';
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
        submission: 'processes.ideamanagement.createAndPublish.submission'
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
      }
    }
  },
  usermanagement: {
    id: 'usermanagement',
    nodes: {
      login: {
        nodeId: 'login',
        title: 'processes.usermanagement.login.title'
      },
      logout: {
        nodeId: 'logout',
        title: 'processes.usermanagement.logout.title'
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
      }
    }
  },
  registrationmanagement: {
    id: 'registrationmanagement',
    nodes: {
      registration: {
        nodeId: 'registration',
        title: 'processes.registrationmanagement.registration.title',
        description: 'processes.registrationmanagement.registration.title'
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
  secondary: 'secondary',
  entity: 'entity',
  global: 'global',
  other: 'other',
  menu: 'menu',
  mainMenu: 'main-menu',
  site: 'site'
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
    submitted: 'submitted'
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
  'glyphicon glyphicon-share': iconAdapter('mdi-set mdi-earth')
};

export const ENTITIES_ICONS = {
  Idea: iconAdapter('mdi-set mdi-lightbulb'),
  default: iconAdapter('mdi-set mdi-pound')
};