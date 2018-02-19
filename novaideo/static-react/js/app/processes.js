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
        description: 'evaluation.supportTheIdea'
      },
      oppose: {
        nodeId: 'oppose',
        description: 'evaluation.opposeTheIdea'
      },
      withdrawToken: {
        nodeId: 'withdraw_token',
        description: 'evaluation.withdrawTokenIdea'
      },
      delete: {
        nodeId: 'delidea'
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
      delete: { nodeId: 'remove' }
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