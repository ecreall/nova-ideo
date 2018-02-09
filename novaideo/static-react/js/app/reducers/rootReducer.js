import { combineReducers } from 'redux';
import { i18nReducer } from 'react-redux-i18n';
import update from 'immutability-helper';
import { reducer as formReducer } from 'redux-form';

import getAllAdapters from '../components/vendor/utils';
import theme from '../theme';
import * as constants from '../constants';

const initialUserTest = {
  token: '0bfa81ae040541aeb65df6d8a710631e',
  loadingState: 'completed'
};
export const user = (state = initialUserTest, action) => {
  switch (action.type) {
  case `${constants.LOGIN}_FULFILLED`: {
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
  case `${constants.LOGIN}_PENDING`: {
    return {
      token: state.token,
      loadingState: 'pending'
    };
  }
  case `${constants.LOGIN}_REJECTED`: {
    return {
      token: state.token,
      loadingState: 'error'
    };
  }
  case constants.LOGIN_IN_PROGRESS: {
    return {
      token: state.token,
      loadingState: 'progress'
    };
  }
  case `${constants.LOGOUT}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        token: undefined,
        loadingState: 'completed'
      };
    }

    return state;
  }

  case `${constants.LOGOUT}_REJECTED`: {
    return {
      token: state.token,
      loadingState: 'error'
    };
  }

  case `${constants.INIT_INSTANCE}_REJECTED`: {
    return {
      token: state.token,
      loadingState: 'error'
    };
  }

  case `${constants.INIT_INSTANCE}_FULFILLED`: {
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

export const search = (state = { text: '' }, action) => {
  switch (action.type) {
  case constants.SEARCH_ENTITIES: {
    return {
      text: action.text
    };
  }
  default:
    return state;
  }
};

export const adapters = (state = { theme: theme }, action) => {
  switch (action.type) {
  case `${constants.SET_INSTANCE}_FULFILLED`: {
    let instanceId;
    if (action.payload) instanceId = action.payload.app;
    return getAllAdapters(instanceId);
  }
  case constants.LOAD_ADAPTERS: {
    return getAllAdapters(action.instanceId);
  }
  default:
    return state;
  }
};

export const network = (
  state = {
    isConnected: false,
    isLogged: false,
    url: { error: false, messages: [] }
  },
  action
) => {
  switch (action.type) {
  case constants.SET_CONNECTION_STATE: {
    return {
      isConnected: action.isConnected,
      isLogged: state.isLogged,
      url: { error: false, messages: [] }
    };
  }

  case constants.SET_URL_STATE: {
    return {
      isConnected: state.isConnected,
      isLogged: state.isLogged,
      url: { error: action.error, messages: action.messages }
    };
  }
  case `${constants.LOGIN}_REJECTED`: {
    return {
      isConnected: state.isConnected,
      isLogged: false,
      url: { error: true, messages: ['Login failed'] }
    };
  }
  case `${constants.LOGOUT}_REJECTED`: {
    return {
      isConnected: state.isConnected,
      isLogged: state.isLogged,
      url: { error: true, messages: ['Logout failed'] }
    };
  }
  case `${constants.INIT_INSTANCE}_REJECTED`: {
    return {
      isConnected: state.isConnected,
      isLogged: state.isLogged,
      url: { error: true, messages: ['Logout failed'] }
    };
  }
  case `${constants.LOGIN}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        isConnected: state.isConnected,
        isLogged: true,
        url: state.url
      };
    }
    return state;
  }
  case `${constants.LOGOUT}_FULFILLED`: {
    if (action.payload && action.payload.status) {
      return {
        isConnected: state.isConnected,
        isLogged: false,
        url: state.url
      };
    }

    return state;
  }
  case `${constants.INIT_INSTANCE}_FULFILLED`: {
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
  case `${constants.SET_INSTANCE}_FULFILLED`: {
    if (action.payload) {
      const instanceId = action.payload.app;
      const currentEntry = state[instanceId] || { data: {}, userPreferences: {} };
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
  case constants.SET_THEME: {
    const instanceId = action.instance.id;
    let currentEntry = state[instanceId];
    if (!currentEntry) {
      currentEntry = {
        data: {
          id: instanceId,
          url: action.instance.url,
          isPrivate: action.instance.isPrivate,
          logo: action.instance.logo,
          title: action.instance.title
        },
        userPreferences: {}
      };
    }
    const newEntry = {
      ...currentEntry,
      userPreferences: { ...currentEntry.userPreferences, appColor: action.color }
    };
    const newStateEntry = {};
    newStateEntry[instanceId] = newEntry;
    return update(state, { $merge: newStateEntry });
  }
  case constants.UPDATE_TOKEN: {
    const instanceId = action.instance.id;
    let currentEntry = state[instanceId];
    if (!currentEntry) {
      currentEntry = {
        data: {
          id: instanceId,
          url: action.instance.url,
          isPrivate: action.instance.isPrivate,
          logo: action.instance.logo,
          title: action.instance.title
        },
        userPreferences: {}
      };
    }
    const newEntry = {
      ...currentEntry,
      data: {
        ...currentEntry.data,
        token: action.token
      }
    };
    const newStateEntry = {};
    newStateEntry[instanceId] = newEntry;
    return update(state, { $merge: newStateEntry });
  }
  case constants.UPDATE_NAVIGATION: {
    const navigation = state.navigation;
    const newPrevious = action.updatePrevious ? navigation.location : navigation.previous;
    return { ...state, ...{ navigation: { location: action.location, previous: newPrevious } } };
  }
  default:
    return state;
  }
};

export const globalProps = (state = {}, action) => {
  switch (action.type) {
  case constants.UPDATE_GLOBAL_PROPS: {
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
    channel: undefined,
    subject: undefined,
    right: {
      open: false,
      componentId: undefined
    }
  }
};

export const apps = (state = initialAppsState, action) => {
  switch (action.type) {
  case constants.UPDATE_APP: {
    const app = action.app;
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
  }
  case constants.OPEN_DRAWER: {
    return { ...state, ...{ drawer: { open: true, app: action.app } } };
  }
  case constants.CLOSE_DRAWER: {
    return { ...state, ...{ drawer: { open: false, app: undefined } } };
  }
  case constants.OPEN_CHATAPP: {
    const config = action.config;
    let drawer = true;
    if ('drawer' in config) {
      drawer = config.drawer;
      delete config.drawer;
    }
    return {
      ...state,
      ...{ drawer: { open: drawer, app: 'chatApp' } },
      ...{ chatApp: { ...state.chatApp, ...{ open: true }, ...action.config } }
    };
  }
  case constants.CLOSE_CHATAPP: {
    const defaultConfig = {
      channel: undefined,
      subject: undefined,
      right: {
        open: false,
        componentId: undefined
      }
    };
    const actionConfig = action.config || {};
    let drawer = true;
    if ('drawer' in actionConfig) {
      drawer = actionConfig.drawer;
      delete actionConfig.drawer;
    }
    const config = { ...defaultConfig, ...actionConfig };
    return {
      ...state,
      ...{ drawer: { open: drawer, app: undefined } },
      ...{ chatApp: { ...state.chatApp, ...{ open: false }, ...config } }
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
  network: network,
  adapters: adapters,
  globalProps: globalProps,
  history: history,
  apps: apps,
  form: formReducer
});