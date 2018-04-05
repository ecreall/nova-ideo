/* eslint-disable import/prefer-default-export */
import * as constants from '../constants';
import { asyncLogin, asyncLogout } from '../utils/user';

export const loadAdapters = (instanceId) => {
  return {
    type: constants.LOAD_ADAPTERS,
    instanceId: instanceId
  };
};

// export const setInstance = (instanceId) => {
//   return {
//     payload: asyncGetInstanceInfo(instanceId),
//     type: constants.SET_INSTANCE
//   };
// };

export const initSelection = () => {
  return {
    type: constants.IN_PROGRESS
  };
};

export const userLogin = (login, password, token) => {
  return {
    payload: asyncLogin(login, password, token),
    type: constants.LOGIN
  };
};

export const updateUserToken = (token) => {
  return {
    token: token,
    type: constants.UPDATE_TOKEN
  };
};

export const initLogin = () => {
  return {
    type: constants.LOGIN_IN_PROGRESS
  };
};

export const searchEntities = (text) => {
  return {
    type: constants.SEARCH_ENTITIES,
    text: text
  };
};

export const logout = () => {
  return {
    payload: asyncLogout(),
    type: constants.LOGOUT
  };
};

// export const initInstance = (instance) => {
//   return {
//     payload: asyncLogout(instance),
//     type: constants.INIT_INSTANCE
//   };
// };

export const setConnectionState = (isConnected) => {
  return {
    type: constants.SET_CONNECTION_STATE,
    isConnected: isConnected
  };
};

export const setURLState = (error, messages) => {
  return {
    type: constants.SET_URL_STATE,
    error: error,
    messages: messages
  };
};

export const setTheme = (instance, color) => {
  return {
    type: constants.SET_THEME,
    instance: instance,
    color: color
  };
};

export const updateGlobalProps = (props) => {
  return {
    type: constants.UPDATE_GLOBAL_PROPS,
    props: props
  };
};

export const updateApp = (app, data) => {
  return {
    type: constants.UPDATE_APP,
    app: app,
    data: data
  };
};

export const openDrawer = (app) => {
  return {
    type: constants.OPEN_DRAWER,
    app: app
  };
};

export const closeDrawer = () => {
  return {
    type: constants.CLOSE_DRAWER
  };
};

export const openChatApp = (config) => {
  return {
    type: constants.OPEN_CHATAPP,
    config: config
  };
};

export const closeChatApp = (config) => {
  return {
    type: constants.CLOSE_CHATAPP,
    config: config
  };
};

export const openCollaborationRight = (config) => {
  return {
    type: constants.OPEN_COLLABORATION_RIGHT,
    config: config
  };
};

export const closeCollaborationRight = (config) => {
  return {
    type: constants.CLOSE_COLLABORATION_RIGHT,
    config: config
  };
};

export const updateChatAppRight = (config) => {
  return {
    type: constants.UPDATE_CHATAPP_RIGHT,
    config: config
  };
};

export const updateCollaborationAppRight = (config) => {
  return {
    type: constants.UPDATE_COLLABORATION_RIGHT,
    config: config
  };
};

export const updateNavigation = (location, updatePrevious) => {
  return {
    type: constants.UPDATE_NAVIGATION,
    location: location,
    updatePrevious: updatePrevious
  };
};