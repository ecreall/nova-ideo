import * as actionTypes from './actionTypes';

export const loadAdapters = (instanceId) => {
  return {
    type: actionTypes.LOAD_ADAPTERS,
    instanceId: instanceId
  };
};

export const updateGlobalProps = (props) => {
  return {
    type: actionTypes.UPDATE_GLOBAL_PROPS,
    props: props
  };
};

export const updateNavigation = (location, updatePrevious) => {
  return {
    type: actionTypes.UPDATE_NAVIGATION,
    location: location,
    updatePrevious: updatePrevious
  };
};

export const setConnectionState = (isConnected) => {
  return {
    type: actionTypes.SET_CONNECTION_STATE,
    isConnected: isConnected
  };
};

export const setURLState = (error, messages) => {
  return {
    type: actionTypes.SET_URL_STATE,
    error: error,
    messages: messages
  };
};

// export const setInstance = (instanceId) => {
//   return {
//     payload: asyncGetInstanceInfo(instanceId),
//     type: actionTypes.SET_INSTANCE
//   };
// };

// export const initInstance = (instance) => {
//   return {
//     payload: asyncLogout(instance),
//     type: actionTypes.INIT_INSTANCE
//   };
// };