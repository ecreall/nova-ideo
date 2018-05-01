/* eslint-disable global-require */

export const STATIC_URL = '/novaideostatic-react/';

export const DEFAULT_LOGO = STATIC_URL + require('./assets/novaideo_logo.png');

export const STICKER_WOMEN_1 = STATIC_URL + require('./assets/sticker-women-1.svg');

export const STICKER_WOMEN_2 = STATIC_URL + require('./assets/sticker-women-2.svg');

export const STICKER_MAN_1 = STATIC_URL + require('./assets/sticker-man-1.svg');

export const STICKER_MAN_2 = STATIC_URL + require('./assets/sticker-man-2.svg');

export const NO_COMMENT = STATIC_URL + require('./assets/no-comment.svg');

export const NOT_LOGGED = STATIC_URL + require('./assets/not-logged.svg');

export const CT_COMMENT = STATIC_URL + require('./assets/ct-comment.svg');

export const USER_BACKGROUND = STATIC_URL + require('./assets/background-person.png');

export const PICKER_EMOJI_SHEET_APPLE_32 = STATIC_URL + require('./assets/sheets/picker_apple_32.png');

export const CONVERTOR_EMOJI_SHEET_APPLE_32 = STATIC_URL + require('./assets/sheets/convertor_apple_32.png');

export const PRIVACY_POLICY_URL_FR = 'https://www.iubenda.com/privacy-policy/8216991';

export const PRIVACY_POLICY_URL_EN = 'https://www.iubenda.com/privacy-policy/8216928';

export const PRESENTATION_TEXT_LEN = 300;

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

export const FILES_ICONS = {
  PDF: {
    icon: 'pdf-icon mdi-set mdi-file-pdf',
    id: 'pdf-icon'
  },
  SPREADSHEET: {
    icon: 'excel-icon mdi-set mdi-file-excel',
    id: 'excel-icon'
  },
  PRESENTATION: {
    icon: 'presentation-icon mdi-set mdi-file-powerpoint',
    id: 'presentation-icon'
  },
  TEXT: {
    icon: 'document-icon mdi-set mdi-file-document',
    id: 'document-icon'
  },
  PLAIN: {
    icon: 'document-icon mdi-set mdi-file-document',
    id: 'document-icon'
  },
  OGG: {
    icon: 'document-icon mdi-set mdi-microphone',
    id: 'document-icon'
  },
  WEBM: {
    icon: 'document-icon mdi-set mdi-microphone',
    id: 'document-icon'
  }
};