import classNames from 'classnames';
import React from 'react';

import { bsClass, getClassSet, prefix, splitBsProps } from './utils/overlayUtils';

const defaultProps = {
  placement: 'right'
};

class Tooltip extends React.Component {
  render() {
    const {
      placement,
      positionTop,
      positionLeft,
      arrowOffsetTop,
      arrowOffsetLeft,
      className,
      style,
      children,
      ...props
    } = this.props;

    const [bsProps, elementProps] = splitBsProps(props);

    const classes = {
      ...getClassSet(bsProps),
      [placement]: true
    };

    const outerStyle = {
      top: positionTop,
      left: positionLeft,
      ...style
    };

    const arrowStyle = {
      top: arrowOffsetTop,
      left: arrowOffsetLeft
    };

    return (
      <div {...elementProps} role="tooltip" className={classNames(className, classes)} style={outerStyle}>
        <div className={prefix(bsProps, 'arrow')} style={arrowStyle} />

        <div className={prefix(bsProps, 'inner')}>
          {children}
        </div>
      </div>
    );
  }
}

Tooltip.defaultProps = defaultProps;

export default bsClass('tooltip', Tooltip);