/* eslint-disable global-require */

export const STATIC_URL = '/novaideostatic-react/';

export const DEFAULT_LOGO = STATIC_URL + require('./assets/novaideo_logo.png');

export const PICKER_EMOJI_SHEET_APPLE_32 = STATIC_URL + require('./assets/sheets/picker_apple_32.png');

export const CONVERTOR_EMOJI_SHEET_APPLE_32 = STATIC_URL + require('./assets/sheets/convertor_apple_32.png');

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

export const UPDATE_CHATAPP_RIGHT = 'UPDATE_CHATAPP_RIGHT';

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

export const STYLE_CONST = {
  drawerDuration: '50ms',
  drawerWidth: 220
};

export const COMMENTS_TIME_INTERVAL = 5; // 5 minutes

export const APOLLO_NETWORK_STATUS = {
  /**
   * The query has never been run before and the query is now currently running. A query will still
   * have this network status even if a partial data result was returned from the cache, but a
   * query was dispatched anyway.
   */
  loading: 1,

  /**
   * If `setVariables` was called and a query was fired because of that then the network status
   * will be `setVariables` until the result of that query comes back.
   */
  setVariables: 2,

  /**
   * Indicates that `fetchMore` was called on this query and that the query created is currently in
   * flight.
   */
  fetchMore: 3,

  /**
   * Similar to the `setVariables` network status. It means that `refetch` was called on a query
   * and the refetch request is currently in flight.
   */
  refetch: 4,

  /**
   * No request is in flight for this query, and no errors happened. Everything is OK.
   */
  ready: 7
};