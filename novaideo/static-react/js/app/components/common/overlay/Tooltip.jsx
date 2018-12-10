import classNames from 'classnames';
import React from 'react';

import {
  bsClass, getClassSet, prefix, splitBsProps
} from './utils/overlayUtils';

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
      innerClassName,
      arrowClassName,
      style,
      innerStyle,
      color,
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
    const placementCapitalize = placement.charAt(0).toUpperCase() + placement.slice(1);
    const borderColorLable = `border${placementCapitalize}Color`;
    const arrowStyle = {
      top: arrowOffsetTop,
      left: arrowOffsetLeft,
      [borderColorLable]: color
    };

    return (
      <div {...elementProps} role="tooltip" className={classNames(className, classes)} style={outerStyle}>
        <div className={classNames(arrowClassName, prefix(bsProps, 'arrow'))} style={arrowStyle} />
        <div
          className={classNames(innerClassName, prefix(bsProps, 'inner'))}
          style={{
            backgroundColor: color,
            ...innerStyle
          }}
        >
          {children}
        </div>
      </div>
    );
  }
}

Tooltip.defaultProps = defaultProps;

export default bsClass('tooltip', Tooltip);