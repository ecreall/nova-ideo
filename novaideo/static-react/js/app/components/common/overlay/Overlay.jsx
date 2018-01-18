import classNames from 'classnames';
import React, { cloneElement } from 'react';
import BaseOverlay from 'react-overlays/lib/Overlay';

import Fade from './Fade';

const defaultProps = {
  animation: Fade,
  rootClose: false,
  show: false,
  placement: 'right'
};

class Overlay extends React.Component {
  render() {
    const { animation, children, ...props } = this.props;

    const transition = animation === true ? Fade : animation || null;

    let child;

    if (!transition) {
      child = cloneElement(children, {
        className: classNames(children.props.className, 'in')
      });
    } else {
      child = children;
    }

    return (
      <BaseOverlay {...props} transition={transition}>
        {child}
      </BaseOverlay>
    );
  }
}

Overlay.defaultProps = defaultProps;

export default Overlay;