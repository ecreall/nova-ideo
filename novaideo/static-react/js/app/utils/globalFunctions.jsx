import React from 'react';
import Moment from 'moment';
import { I18n } from 'react-redux-i18n';
import Icon from '@material-ui/core/Icon';
import classNames from 'classnames';
import * as Vibrant from 'node-vibrant';

import * as constants from '../constants';

export const calculatePercentage = (value1, value2) => {
  return Math.round(((value1 * 100) / value2) * 100) / 100;
};

/*
  Handrolled instead of using lodash
  Because lodash/capitalize lowercases everything else
*/
export const capitalize = (s) => {
  return s.charAt(0).toUpperCase() + s.slice(1);
};

export const getDocumentScrollTop = () => {
  return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
};

export const getDomElementOffset = (el) => {
  const rect = el.getBoundingClientRect();
  const scrollTop = getDocumentScrollTop();
  const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0;
  return { top: rect.top + scrollTop, left: rect.left + scrollLeft };
};

export const computeDomElementOffset = (ref, offset) => {
  // inspired from jquery.setOffset
  const curOffset = getDomElementOffset(ref);
  const curCSS = window.getComputedStyle(ref);
  const curTop = parseFloat(curCSS.top) || 0;
  const curLeft = parseFloat(curCSS.left) || 0;
  const result = { top: curTop, left: curLeft };

  if ('top' in offset) result.top = offset.top - curOffset.top + curTop;
  if ('left' in offset) result.left = offset.left - curOffset.left + curLeft;
  return result;
};

export const createEvent = (typeArg, dispatch = false, eventInit = { bubbles: false, cancelable: false }) => {
  // inspired from https://developer.mozilla.org/en-US/docs/Web/API/Event/Event
  const event = document.createEvent('Event'); // we can't use 'new Event()' because ie
  event.initEvent(typeArg, eventInit.bubbles, eventInit.cancelable);
  if (dispatch) document.dispatchEvent(event);
  return event;
};

/*
  Get basename from a unix or windows path
*/
export const getBasename = (path) => {
  return path
    .split('\\')
    .pop()
    .split('/')
    .pop();
};

export const hashLinkScroll = () => {
  const { hash } = window.location;
  if (hash !== '') {
    const id = hash.replace('#', '');
    // Push onto callback queue so it runs after the DOM is updated,
    // this is required when navigating from a different page so that
    // the element is rendered on the page before trying to getElementById.
    setTimeout(() => {
      const element = document.getElementById(id);
      if (element) {
        const offset = getDomElementOffset(element).top - 160;
        window.scrollTo({ top: offset, left: 0, behavior: 'smooth' });
      }
    }, 0);
  }
};

export const hexToRgb = (c) => {
  if (!c) return '';
  const hex = c.replace(/[^0-9A-F]/gi, '');
  const bigint = parseInt(hex, 16);
  const r = (bigint >> 16) & 255; // eslint-disable-line
  const g = (bigint >> 8) & 255; // eslint-disable-line
  const b = bigint & 255; // eslint-disable-line

  return [r, g, b].join();
};

export const isMobile = {
  android: () => {
    return navigator.userAgent.match(/Android/i);
  },
  blackberry: () => {
    return navigator.userAgent.match(/BlackBerry/i);
  },
  ios: () => {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i);
  },
  opera: () => {
    return navigator.userAgent.match(/Opera Mini/i);
  },
  windows: () => {
    return navigator.userAgent.match(/IEMobile/i);
  },
  any: () => {
    return isMobile.android() || isMobile.blackberry() || isMobile.ios() || isMobile.opera() || isMobile.windows();
  }
};

export const REGEXP = {
  youtube: /(?:youtube\.com\/(?:[^/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?/ ]{11})/i,
  sketchfab: /(?:sketchfab\.com\/(show|models)\/(.*))/i
};

export function initalsGenerator(name) {
  return name
    .split(' ')
    .map((part) => {
      return part.charAt(0).toUpperCase();
    })
    .join('');
}

export function getFormattedDate(date, defaultFormat, config = { today: 'date.todayFormat', yesterday: 'date.yesterdayFormat' }) {
  const today = Moment();
  const isToday = today.isSame(Moment(date), 'day');
  const yesterday = today.subtract(1, 'days').startOf('day');
  const isYesterday = yesterday.isSame(Moment(date), 'day');
  const format = (isToday && config.today) || (isYesterday && config.yesterday) || defaultFormat;
  return Moment(date).format(I18n.t(format));
}

export const iconAdapter = (name) => {
  return (props) => {
    const { className, ...iconProps } = props;
    return <Icon className={classNames(name, className)} {...iconProps} />;
  };
};

export const getFileType = (type) => {
  if (!type) return undefined;
  const mimetypeParts = type ? type.split('/') : [];
  const mimetype = mimetypeParts.length > 1 ? mimetypeParts[1] : mimetypeParts[0];
  const documentTypeParts = mimetype.split('.');
  return documentTypeParts[documentTypeParts.length - 1].toUpperCase();
};

export function getImagePalette(url) {
  return Vibrant.from(url)
    .getPalette()
    .then((response) => {
      const keys = Object.keys(response);
      const addPalette = (acc, paletteName) => {
        return {
          ...acc,
          [paletteName]: response[paletteName] && response[paletteName].getHex()
        };
      };
      const colorPallete = keys.reduce(addPalette, {});
      return colorPallete;
    });
}

export function arrayToDict(list) {
  const result = {};
  const reducer = (accumulator, currentValue) => {
    accumulator[currentValue] = currentValue;
    return accumulator;
  };
  list.reduce(reducer, result);
  return result;
}

export function truncateText(text, len = constants.PRESENTATION_TEXT_LEN) {
  return `${text.substring(0, len)}...`;
}