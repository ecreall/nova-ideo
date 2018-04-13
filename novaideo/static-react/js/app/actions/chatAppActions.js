import * as actionTypes from './actionTypes';

export const updateChatApp = (data) => {
  return {
    type: actionTypes.UPDATE_CHATAPP,
    data: data
  };
};

export const updateChatAppRight = (config) => {
  return {
    type: actionTypes.UPDATE_CHATAPP_RIGHT,
    config: config
  };
};

export const openChatApp = (config) => {
  return {
    type: actionTypes.OPEN_CHATAPP,
    config: config
  };
};

export const closeChatApp = (config) => {
  return {
    type: actionTypes.CLOSE_CHATAPP,
    config: config
  };
};

export const addChatAppIntegration = () => {
  return {
    type: actionTypes.ADD_CHATAPP_INTEGRATION
  };
};

export const removeChatAppIntegration = () => {
  return {
    type: actionTypes.REMOVE_CHATAPP_INTEGRATION
  };
};