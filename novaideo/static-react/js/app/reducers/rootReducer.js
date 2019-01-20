import { combineReducers } from 'redux';
import { i18nReducer } from 'react-redux-i18n';
import update from 'immutability-helper';
import { reducer as formReducer } from 'redux-form';

import getAllAdapters from '../components/vendor/utils';
import theme from '../theme';
import * as actionTypes from '../actions/actionTypes';

// 4b3fc3b2e8b64e3ab95dc38122737f67
// 0bfa81ae040541aeb65df6d8a710631e
// 03515792dedc4f8bbb1c77cdb0142fd6

const initialUserTest = {
  token: '',
  loadingState: 'completed'
};
export const user = (state = initialUserTest, action) => {
  switch (action.type) {
  case actionTypes.UPDATE_TOKEN: {
    return {
      token: action.token,
      loadingState: 'completed'
    };
  }
  case `${actionTypes.LOGIN}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        token: action.payload.token,
        loadingState: 'completed'
      };
    }
    return {
      token: state.token,
      loadingState: 'error'
    };
  }
  case `${actionTypes.LOGIN}_PENDING`: {
    return {
      token: state.token,
      loadingState: 'pending'
    };
  }
  case `${actionTypes.LOGIN}_REJECTED`: {
    return {
      token: state.token,
      loadingState: 'error'
    };
  }
  case actionTypes.LOGIN_IN_PROGRESS: {
    return {
      token: state.token,
      loadingState: 'progress'
    };
  }
  case `${actionTypes.LOGOUT}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        token: undefined,
        loadingState: 'completed'
      };
    }

    return state;
  }

  case `${actionTypes.LOGOUT}_REJECTED`: {
    return {
      token: state.token,
      loadingState: 'error'
    };
  }

  case `${actionTypes.INIT_INSTANCE}_REJECTED`: {
    return {
      token: state.token,
      loadingState: 'error'
    };
  }

  case `${actionTypes.INIT_INSTANCE}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        token: undefined,
        loadingState: 'completed'
      };
    }
    return state;
  }

  default:
    return state;
  }
};

export const search = (state = {}, action) => {
  switch (action.type) {
  case actionTypes.SEARCH_ENTITIES: {
    const { id, text } = action;
    return {
      ...state,
      [id]: {
        text: text
      }
    };
  }
  default:
    return state;
  }
};

export const filter = (state = {}, action) => {
  switch (action.type) {
  case actionTypes.FILTER_ENTITIES: {
    const { id } = action;
    return {
      ...state,
      [id]: {
        ...action.filter
      }
    };
  }
  case actionTypes.FILTER_CLEAR: {
    const { id } = action;
    const newState = { ...state };
    delete newState[id];
    return newState;
  }
  default:
    return state;
  }
};

export const adapters = (state = { theme: theme }, action) => {
  switch (action.type) {
  case `${actionTypes.SET_INSTANCE}_FULFILLED`: {
    let instanceId;
    if (action.payload) instanceId = action.payload.app;
    return getAllAdapters(instanceId);
  }
  case actionTypes.LOAD_ADAPTERS: {
    return getAllAdapters(action.instanceId);
  }
  default:
    return state;
  }
};

export const network = (
  state = {
    isConnected: true,
    isLogged: false,
    url: { error: false, messages: [] }
  },
  action
) => {
  switch (action.type) {
  case actionTypes.SET_CONNECTION_STATE: {
    return {
      isConnected: action.isConnected,
      isLogged: state.isLogged,
      url: { error: false, messages: [] }
    };
  }

  case actionTypes.SET_URL_STATE: {
    return {
      isConnected: state.isConnected,
      isLogged: state.isLogged,
      url: { error: action.error, messages: action.messages }
    };
  }
  case `${actionTypes.LOGIN}_REJECTED`: {
    return {
      isConnected: state.isConnected,
      isLogged: false,
      url: { error: true, messages: ['Login failed'] }
    };
  }
  case `${actionTypes.LOGOUT}_REJECTED`: {
    return {
      isConnected: state.isConnected,
      isLogged: state.isLogged,
      url: { error: true, messages: ['Logout failed'] }
    };
  }
  case `${actionTypes.INIT_INSTANCE}_REJECTED`: {
    return {
      isConnected: state.isConnected,
      isLogged: state.isLogged,
      url: { error: true, messages: ['Logout failed'] }
    };
  }
  case `${actionTypes.LOGIN}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        isConnected: state.isConnected,
        isLogged: true,
        url: state.url
      };
    }
    return state;
  }
  case actionTypes.UPDATE_TOKEN: {
    return {
      isConnected: true,
      isLogged: true,
      url: state.url
    };
  }
  case `${actionTypes.LOGOUT}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        isConnected: state.isConnected,
        isLogged: false,
        url: state.url
      };
    }

    return state;
  }
  case `${actionTypes.INIT_INSTANCE}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        isConnected: state.isConnected,
        isLogged: false,
        url: state.url
      };
    }

    return state;
  }
  default:
    return state;
  }
};

const initNavigationState = {
  navigation: {
    location: '/',
    previous: undefined
  }
};

export const history = (state = initNavigationState, action) => {
  switch (action.type) {
  case `${actionTypes.SET_INSTANCE}_FULFILLED`: {
    if (action.payload) {
      const instanceId = action.payload.app;
      const currentEntry = state[instanceId] || {};
      const newEntry = {
        ...currentEntry,
        data: {
          ...currentEntry.data,
          id: instanceId,
          url: action.payload.url,
          isPrivate: action.payload.type === 'private',
          logo: action.payload.logoUrl,
          title: action.payload.title
        }
      };
      const newStateEntry = {};
      newStateEntry[instanceId] = newEntry;
      return update(state, { $merge: newStateEntry });
    }
    return state;
  }
  // case actionTypes.UPDATE_TOKEN: {
  //   const instanceId = action.instance.siteId;
  //   let currentEntry = state[instanceId];
  //   if (!currentEntry) {
  //     currentEntry = {
  //       data: {
  //         id: instanceId,
  //         url: windows.location,
  //         isPrivate: action.instance.onlyForMembers,
  //         logo: action.instance.logo,
  //         title: action.instance.title
  //       }
  //     };
  //   }
  //   const newEntry = {
  //     ...currentEntry,
  //     data: {
  //       ...currentEntry.data,
  //       token: action.token
  //     }
  //   };
  //   const newStateEntry = {};
  //   newStateEntry[instanceId] = newEntry;
  //   return update(state, { $merge: newStateEntry });
  // }
  case actionTypes.UPDATE_NAVIGATION: {
    const { navigation } = state;
    const newPrevious = action.updatePrevious ? navigation.location : navigation.previous;
    return { ...state, navigation: { location: action.location, previous: newPrevious } };
  }
  default:
    return state;
  }
};

export const globalProps = (state = {}, action) => {
  switch (action.type) {
  case actionTypes.UPDATE_GLOBAL_PROPS: {
    return { ...state, ...action.props };
  }
  default:
    return state;
  }
};

const initialAppsState = {
  drawer: {
    open: true,
    app: undefined
  },
  chatApp: {
    open: false,
    integrations: 0,
    channel: undefined,
    subject: undefined,
    right: {
      open: false,
      componentId: undefined,
      full: false,
      props: {}
    }
  },
  collaborationApp: {
    right: {
      open: false,
      componentId: undefined,
      full: false,
      props: {}
    }
  }
};

export const apps = (state = initialAppsState, action) => {
  const updateApp = (app) => {
    let currentEntry = state[app];
    if (!currentEntry) {
      currentEntry = {
        ...action.data
      };
    }
    const newEntry = {
      ...currentEntry,
      ...action.data
    };
    const newStateEntry = {};
    newStateEntry[app] = newEntry;
    return update(state, { $merge: newStateEntry });
  };

  switch (action.type) {
  case actionTypes.UPDATE_APP: {
    const { app } = action;
    return updateApp(app);
  }
  case actionTypes.UPDATE_COLLABORATIONAPP: {
    return updateApp('collaborationApp');
  }
  case actionTypes.UPDATE_CHATAPP: {
    return updateApp('chatApp');
  }
  case actionTypes.OPEN_DRAWER: {
    return { ...state, drawer: { open: true, app: action.app } };
  }
  case actionTypes.CLOSE_DRAWER: {
    return { ...state, drawer: { open: false, app: undefined } };
  }
  case actionTypes.TOGGLE_DRAWER: {
    return { ...state, drawer: { ...state.drawer, open: !state.drawer.open } };
  }
  case actionTypes.OPEN_CHATAPP: {
    const { config } = action;
    const drawerConfigured = 'drawer' in config;
    const { drawer } = drawerConfigured ? config : state;
    if (drawerConfigured) {
      delete config.drawer;
    }
    return {
      ...state,
      drawer: { ...drawer, app: 'chatApp' },
      chatApp: { ...state.chatApp, open: true, ...action.config }
    };
  }
  case actionTypes.ADD_CHATAPP_INTEGRATION: {
    return {
      ...state,
      chatApp: { ...state.chatApp, integrations: state.chatApp.integrations + 1 }
    };
  }
  case actionTypes.REMOVE_CHATAPP_INTEGRATION: {
    let integrations = state.chatApp.integrations - 1;
    integrations = integrations < 0 ? 0 : integrations;
    return {
      ...state,
      chatApp: { ...state.chatApp, integrations: integrations }
    };
  }
  case actionTypes.CLOSE_CHATAPP: {
    const defaultConfig = {
      channel: undefined,
      subject: undefined,
      integrations: 0,
      right: {
        open: false,
        componentId: undefined
      }
    };
    const config = action.config || {};
    const drawerConfigured = 'drawer' in config;
    const { drawer } = drawerConfigured ? config : state;
    if (drawerConfigured) {
      delete config.drawer;
    }
    const actionCconfig = { ...defaultConfig, ...config };
    return {
      ...state,
      drawer: { ...state.drawer, ...drawer },
      chatApp: { ...state.chatApp, open: false, ...actionCconfig }
    };
  }
  case actionTypes.OPEN_COLLABORATION_RIGHT: {
    return {
      ...state,
      collaborationApp: {
        ...state.collaborationApp,
        right: {
          ...state.collaborationApp.right,
          open: true,
          ...action.config
        }
      }
    };
  }
  case actionTypes.CLOSE_COLLABORATION_RIGHT: {
    return {
      ...state,
      collaborationApp: {
        ...state.collaborationApp,
        right: {
          open: false,
          componentId: undefined,
          full: false,
          props: {},
          ...action.config
        }
      }
    };
  }
  case actionTypes.UPDATE_CHATAPP_RIGHT: {
    return {
      ...state,
      chatApp: {
        ...state.chatApp,
        right: { ...state.chatApp.right, ...action.config }
      }
    };
  }
  case actionTypes.UPDATE_COLLABORATION_RIGHT: {
    return {
      ...state,
      collaborationApp: {
        ...state.collaborationApp,
        right: { ...state.collaborationApp.right, ...action.config }
      }
    };
  }
  default:
    return state;
  }
};

export default combineReducers({
  i18n: i18nReducer,
  user: user,
  search: search,
  filter: filter,
  network: network,
  adapters: adapters,
  globalProps: globalProps,
  history: history,
  apps: apps,
  form: formReducer
});