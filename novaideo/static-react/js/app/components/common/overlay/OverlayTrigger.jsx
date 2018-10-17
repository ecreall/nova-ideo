import contains from 'dom-helpers/query/contains';
import React, { cloneElement } from 'react';
import ReactDOM from 'react-dom';
import warning from 'warning';

import Overlay from './Overlay';

import createChainedFunction from './utils/createChainedFunction';

/**
 * Check if value one is inside or equal to the of value
 *
 * @param {string} one
 * @param {string|array} of
 * @returns {boolean}
 */
function isOneOf(one, of) {
  if (Array.isArray(of)) {
    return of.indexOf(one) >= 0;
  }
  return one === of;
}

const defaultProps = {
  defaultOverlayShown: false,
  trigger: ['hover', 'focus']
};

class OverlayTrigger extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.handleToggle = this.handleToggle.bind(this);
    this.handleDelayedShow = this.handleDelayedShow.bind(this);
    this.handleDelayedHide = this.handleDelayedHide.bind(this);
    this.handleHide = this.handleHide.bind(this);

    this.handleMouseOver = (e) => {
      return this.handleMouseOverOut(this.handleDelayedShow, e, 'fromElement');
    };
    this.handleMouseOut = (e) => {
      return this.handleMouseOverOut(this.handleDelayedHide, e, 'toElement');
    };

    this.mountNode = null;

    this.state = {
      show: props.defaultOverlayShown
    };
  }

  componentDidMount() {
    this.mountNode = document.createElement('div');
    this.renderOverlay();
  }

  componentDidUpdate() {
    this.renderOverlay();
  }

  componentWillUnmount() {
    ReactDOM.unmountComponentAtNode(this.mountNode);
    this.mountNode = null;

    clearTimeout(this.hoverShowDelay);
    clearTimeout(this.hoverHideDelay);
  }

  handleDelayedHide() {
    if (this.hoverShowDelay != null) {
      clearTimeout(this.hoverShowDelay);
      this.hoverShowDelay = null;
      return;
    }
    const { delayHide, delay } = this.props;
    const { show } = this.state;
    if (!show || this.hoverHideDelay != null) {
      return;
    }

    const timeout = delayHide != null ? delayHide : delay;

    if (!timeout) {
      this.hide();
      return;
    }

    this.hoverHideDelay = setTimeout(() => {
      this.hoverHideDelay = null;
      this.hide();
    }, timeout);
  }

  handleDelayedShow() {
    if (this.hoverHideDelay != null) {
      clearTimeout(this.hoverHideDelay);
      this.hoverHideDelay = null;
      return;
    }
    const { delayShow, delay } = this.props;
    const { show } = this.state;
    if (show || this.hoverShowDelay != null) {
      return;
    }

    const timeout = delayShow != null ? delayShow : delay;

    if (!timeout) {
      this.show();
      return;
    }

    this.hoverShowDelay = setTimeout(() => {
      this.hoverShowDelay = null;
      this.show();
    }, timeout);
  }

  handleHide() {
    this.hide();
  }

  // Simple implementation of mouseEnter and mouseLeave.
  // React's built version is broken: https://github.com/facebook/react/issues/4251
  // for cases when the trigger is disabled and mouseOut/Over can cause flicker
  // moving from one child element to another.
  handleMouseOverOut(handler, e, relatedNative) {
    const target = e.currentTarget;
    const related = e.relatedTarget || e.nativeEvent[relatedNative];

    if ((!related || related !== target) && !contains(target, related)) {
      handler(e);
    }
  }

  handleToggle() {
    const { show } = this.state;
    if (show) {
      this.hide();
    } else {
      this.show();
    }
  }

  hide() {
    this.setState({ show: false });
  }

  makeOverlay(overlay, props) {
    const { show } = this.state;
    return (
      <Overlay {...props} show={show} onHide={this.handleHide} target={this}>
        {overlay}
      </Overlay>
    );
  }

  show() {
    this.setState({ show: true });
  }

  renderOverlay() {
    ReactDOM.unstable_renderSubtreeIntoContainer(this, this.overlay, this.mountNode);
  }

  render() {
    const {
      trigger, overlay, children, onBlur, onClick, onFocus, onMouseOut, onMouseOver, ...props
    } = this.props;
    const { show } = this.state;
    delete props.delay;
    delete props.delayShow;
    delete props.delayHide;
    delete props.defaultOverlayShown;

    const child = React.Children.only(children);
    const childProps = child.props;
    const triggerProps = {};

    if (show) {
      triggerProps['aria-describedby'] = overlay.props.id;
    }

    // FIXME: The logic here for passing through handlers on this component is
    // inconsistent. We shouldn't be passing any of these props through.
    triggerProps.onClick = createChainedFunction(childProps.onClick, onClick);

    if (isOneOf('click', trigger)) {
      triggerProps.onClick = createChainedFunction(triggerProps.onClick, this.handleToggle);
    }

    if (isOneOf('hover', trigger)) {
      warning(
        !(trigger === 'hover'),
        'Specifying only the `"hover"` trigger limits the '
          + 'visibility of the overlay to just mouse users. Consider also '
          + 'including the `"focus"` trigger so that touch and keyboard only '
          + 'users can see the overlay as well.'
      );

      triggerProps.onMouseOver = createChainedFunction(childProps.onMouseOver, onMouseOver, this.handleMouseOver);
      triggerProps.onMouseOut = createChainedFunction(childProps.onMouseOut, onMouseOut, this.handleMouseOut);
    }

    if (isOneOf('focus', trigger)) {
      triggerProps.onFocus = createChainedFunction(childProps.onFocus, onFocus, this.handleDelayedShow);
      triggerProps.onBlur = createChainedFunction(childProps.onBlur, onBlur, this.handleDelayedHide);
    }

    this.overlay = this.makeOverlay(overlay, props);

    return cloneElement(child, triggerProps);
  }
}
OverlayTrigger.defaultProps = defaultProps;

export default OverlayTrigger;