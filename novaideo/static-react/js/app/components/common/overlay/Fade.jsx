import classNames from 'classnames';
import React from 'react';
import Transition, { ENTERED, ENTERING } from 'react-transition-group/Transition';

const defaultProps = {
  in: false,
  timeout: 300,
  mountOnEnter: false,
  unmountOnExit: false,
  appear: false
};

const fadeStyles = {
  [ENTERING]: 'in',
  [ENTERED]: 'in'
};

class Fade extends React.Component {
  render() {
    const { className, children, ...props } = this.props;

    return (
      <Transition {...props}>
        {(status, innerProps) => {
          return React.cloneElement(children, {
            ...innerProps,
            className: classNames('fade', className, children.props.className, fadeStyles[status])
          });
        }}
      </Transition>
    );
  }
}

Fade.defaultProps = defaultProps;

export default Fade;