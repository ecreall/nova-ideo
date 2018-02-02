import urljoin from 'url-join';
import { browserHistory } from 'react-router';

import parse from './literalStringParser';
import { capitalize } from './globalFunctions';
/*
  A global map of routes managed by React front-end.
*/
/* eslint no-template-curly-in-string: "off" */
const routes = {
  root: '',
  messages: 'messages/${channelId}',
  ideas: 'ideas/${ideaId}'
};

const convertToContextualName = (name) => {
  const base = 'ctx';
  const workingName = capitalize(name);
  return base + workingName;
};

const maybePrependSlash = (pre, s) => {
  return pre ? `/${s}` : s;
};

export const getQuery = (query) => {
  if (!query) return '';
  const entries = Object.keys(query).map((key) => {
    return `${key}=${query[key]}`;
  });
  return `?${entries.join('&')}`;
};

export const get = (name, args, query) => {
  const newArgs = args || {};
  const pre = 'preSlash' in newArgs ? newArgs.preSlash : true;
  const isCtx = 'ctx' in newArgs ? newArgs.ctx : false;
  const newName = isCtx ? convertToContextualName(name) : name;
  if (!(newName in routes)) {
    throw Error(`${newName} is not a valid path!`);
  }
  let literal = routes[newName];
  literal = maybePrependSlash(pre, literal);
  return parse(literal, newArgs) + getQuery(query);
};

const basePath = () => {
  return `${window.location.protocol}//${window.location.host}`;
};

export const getFullPath = (name, args, query) => {
  const rel = get(name, { ...args, preSlash: false }, query);
  return urljoin(basePath(), rel);
};

export const getContextual = (name, args, query) => {
  const newArgs = { ...args, ctx: true }; // Do not mutate args!
  return get(name, newArgs, query);
};

export const routeForRouter = (name, isCtx, args, query) => {
  const newArgs = args || {};
  newArgs.slug = '';
  newArgs.preSlash = newArgs.preSlash ? newArgs.preSlash : false;
  if (isCtx) {
    return getContextual(name, newArgs, query);
  }
  return get(name, newArgs, query);
};

export const getCurrentView = () => {
  return window.location.pathname;
};

export const goTo = (url) => {
  browserHistory.replace(url);
};

export const getCurrentLocation = () => {
  return browserHistory.getCurrentLocation().pathname;
};