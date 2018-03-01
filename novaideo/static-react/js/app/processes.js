/* eslint-disable import/prefer-default-export, import/no-extraneous-dependencies */
import StarBorderIcon from 'material-ui-icons/StarBorder';
import StarIcon from 'material-ui-icons/Star';
import HistoryIcon from 'material-ui-icons/History';
import ReportIcon from 'material-ui-icons/Report';
import ReplyIcon from 'material-ui-icons/Reply';
import ModeEditIcon from 'material-ui-icons/ModeEdit';
import DeleteIcon from 'material-ui-icons/Delete';
import QuestionAnswerIcon from 'material-ui-icons/QuestionAnswer';

import { iconAdapter } from './utils/globalFunctions';

export const PROCESSES = {
  ideamanagement: {
    id: 'ideamanagement',
    nodes: {
      create: {
        nodeId: 'creat'
      },
      createAndPublish: { nodeId: 'creatandpublish' },
      comment: { nodeId: 'comment' },
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
      }
    }
  },
  usermanagement: {
    id: 'usermanagement',
    nodes: {
      discuss: { nodeId: 'discuss' },
      generalDiscuss: { nodeId: 'general_discuss' }
    }
  },
  novaideoabstractprocess: {
    id: 'novaideoabstractprocess',
    nodes: {
      select: { nodeId: 'select' },
      deselect: { nodeId: 'deselect' },
      addreaction: { nodeId: 'addreaction' }
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
  menu: 'menu'
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
  'glyphicon glyphicon-trash': DeleteIcon,
  'icon md md-live-help': QuestionAnswerIcon,
  'typcn typcn-pin': iconAdapter('mdi-set mdi-pin'),
  'typcn typcn-pin-outline': iconAdapter('mdi-set mdi-pin-off'),
  'icon novaideo-icon icon-idea': iconAdapter('mdi-set mdi-lightbulb')
};