import * as actionTypes from './actionTypes';
import { asyncLogin, asyncLogout } from '../utils/user';

export const userLogin = (login, password, token) => {
  return {
    payload: asyncLogin(login, password, token),
    type: actionTypes.LOGIN
  };
};

export const userLogout = () => {
  return {
    payload: asyncLogout(),
    type: actionTypes.LOGOUT
  };
};

export const initLogin = () => {
  return {
    type: actionTypes.LOGIN_IN_PROGRESS
  };
};

export const updateUserToken = (token) => {
  return {
    token: token,
    type: actionTypes.UPDATE_TOKEN
  };
};