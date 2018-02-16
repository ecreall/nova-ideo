/* eslint-disable global-require */
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

export const STATIC_URL = '/novaideostatic-react/';

export const DEFAULT_LOGO = STATIC_URL + require('./assets/novaideo_logo.png');

export const UPDATE_APP = 'UPDATE_APP';

export const PRIVACY_POLICY_URL_FR = 'https://www.iubenda.com/privacy-policy/8216991';

export const PRIVACY_POLICY_URL_EN = 'https://www.iubenda.com/privacy-policy/8216928';

export const SET_INSTANCE = 'SET_INSTANCE';

export const IN_PROGRESS = 'IN_PROGRESS';

export const LOGIN_IN_PROGRESS = 'LOGIN_IN_PROGRESS';

export const LOGIN = 'LOGIN';

export const LOGOUT = 'LOGOUT';

export const INIT_INSTANCE = 'INIT_INSTANCE';

export const SEARCH_ENTITIES = 'SEARCH_ENTITIES';

export const SET_CONNECTION_STATE = 'SET_CONNECTION_STATE';

export const SET_URL_STATE = 'SET_URL_STATE';

export const SET_THEME = 'SET_THEME';

export const UPDATE_TOKEN = 'UPDATE_TOKEN';

export const LOAD_ADAPTERS = 'LOAD_ADAPTERS';

export const UPDATE_GLOBAL_PROPS = 'UPDATE_GLOBAL_PROPS';

export const UPDATE_NAVIGATION = 'UPDATE_NAVIGATION';

export const OPEN_DRAWER = 'OPEN_DRAWER';

export const CLOSE_DRAWER = 'CLOSE_DRAWER';

export const OPEN_CHATAPP = 'OPEN_CHATAPP';

export const CLOSE_CHATAPP = 'CLOSE_CHATAPP';

export const SMALL_WIDTH = ['sm', 'xs'];

export const SIZE_MAP = {
  large: 'lg',
  medium: 'md',
  small: 'sm',
  xsmall: 'xs',
  lg: 'lg',
  md: 'md',
  sm: 'sm',
  xs: 'xs'
};

export const LOADING_STATES = {
  pending: 'pending',
  progress: 'progress',
  error: 'error',
  success: 'success'
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

export const STYLE_CONST = {
  drawerDuration: '50ms',
  drawerWidth: 220
};

export const PROCESSES = {
  ideamanagement: {
    id: 'ideamanagement',
    nodes: {
      create: { nodeId: 'creat' },
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
  }
};

export const COMMENTS_ACTIONS = ['comment', 'discuss', 'general_discuss'];

export const COMMENTS_TIME_INTERVAL = 5; // 5 minutes