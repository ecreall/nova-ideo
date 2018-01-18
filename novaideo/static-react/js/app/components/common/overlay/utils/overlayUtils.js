import invariant from 'invariant';
import PropTypes from 'prop-types';

import { SIZE_MAP } from '../../../../constants';

function curry(fn) {
  return (...args) => {
    const last = args[args.length - 1];
    if (typeof last === 'function') {
      return fn(...args);
    }
    return (Component) => {
      return fn(...args, Component);
    };
  };
}

export function prefix(props, variant) {
  const bsClass = (props.bsClass || '').trim();
  invariant(bsClass != null, 'A `bsClass` prop is required for this component');
  return bsClass + (variant ? `-${variant}` : '');
}

export const bsClass = curry((defaultClass, Component) => {
  const propTypes = Component.propTypes || (Component.propTypes = {});
  const defaultProps = Component.defaultProps || (Component.defaultProps = {});

  propTypes.bsClass = PropTypes.string;
  defaultProps.bsClass = defaultClass;

  return Component;
});

export function getClassSet(props) {
  const classes = {
    [prefix(props)]: true
  };

  if (props.bsSize) {
    const bsSize = SIZE_MAP[props.bsSize] || props.bsSize;
    classes[prefix(props, bsSize)] = true;
  }

  if (props.bsStyle) {
    classes[prefix(props, props.bsStyle)] = true;
  }

  return classes;
}

function getBsProps(props) {
  return {
    bsClass: props.bsClass,
    bsSize: props.bsSize,
    bsStyle: props.bsStyle,
    bsRole: props.bsRole
  };
}

function isBsProp(propName) {
  return propName === 'bsClass' || propName === 'bsSize' || propName === 'bsStyle' || propName === 'bsRole';
}

export function splitBsProps(props) {
  const elementProps = {};
  Object.entries(props).forEach(([propName, propValue]) => {
    if (!isBsProp(propName)) {
      elementProps[propName] = propValue;
    }
  });

  return [getBsProps(props), elementProps];
}