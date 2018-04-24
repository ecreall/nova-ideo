import * as actionTypes from './actionTypes';

export const search = (id, text) => {
  return {
    type: actionTypes.SEARCH_ENTITIES,
    text: text,
    id: id
  };
};

export const globalSearch = (text) => {
  return {
    type: actionTypes.SEARCH_ENTITIES,
    text: text,
    id: 'globalSearch'
  };
};

export const updateApp = (app, data) => {
  return {
    type: actionTypes.UPDATE_APP,
    app: app,
    data: data
  };
};

export const updateCollaborationApp = (data) => {
  return {
    type: actionTypes.UPDATE_COLLABORATIONAPP,
    data: data
  };
};

export const updateCollaborationAppRight = (config) => {
  return {
    type: actionTypes.UPDATE_COLLABORATION_RIGHT,
    config: config
  };
};

export const openDrawer = (app) => {
  return {
    type: actionTypes.OPEN_DRAWER,
    app: app
  };
};

export const closeDrawer = () => {
  return {
    type: actionTypes.CLOSE_DRAWER
  };
};

export const toggleDrawer = () => {
  return {
    type: actionTypes.TOGGLE_DRAWER
  };
};

export const openCollaborationRight = (config) => {
  return {
    type: actionTypes.OPEN_COLLABORATION_RIGHT,
    config: config
  };
};

export const closeCollaborationRight = (config) => {
  return {
    type: actionTypes.CLOSE_COLLABORATION_RIGHT,
    config: config
  };
};