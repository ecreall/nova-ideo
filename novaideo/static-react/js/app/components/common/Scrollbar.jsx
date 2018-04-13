// see https://github.com/philipwalton/flexbugs/issues/108 :(
import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import Baron from 'react-baron';

import { createEvent } from '../../utils/globalFunctions';

const styles = {
  clipper: {
    overflow: 'hidden',
    height: '100%',
    position: 'relative'
  },
  scroller: {
    overflowY: 'scroll',
    height: '100%',
    width: 'calc(100% + 15px) !important',
    minWidth: 'calc(100% + 15px) !important',
    position: 'relative',
    paddingRight: 15
  },
  trackVertical: {
    width: '8px !important',
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    height: '100%'
  },
  thumbVertical: {
    zIndex: 1,
    cursor: 'pointer',
    borderRadius: 6,
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    border: '3px solid #fff',
    position: 'absolute',
    right: 0,
    width: 6
  }
};

class Scrollbar extends React.Component {
  componentDidMount() {
    const { reverted } = this.props;
    if (reverted) this.scrollToBottom();
  }

  componentWillUpdate() {
    const { reverted } = this.props;
    if (reverted) this.savePositions();
  }

  componentDidUpdate() {
    const { reverted } = this.props;
    if (reverted) this.scrollToLastPosition();
  }

  scroll = null;

  positions = null;

  savePositions = () => {
    this.positions = this.getScrollValues();
  };

  scrollToLastPosition = () => {
    const scroller = this.scroll.getScroller();
    const scrollHeight = scroller.scrollHeight;
    const positions = this.positions;
    if (positions) {
      const top = scrollHeight - positions.scrollHeight + positions.scrollTop;
      if (top >= 0) {
        this.scrollTo(top);
      }
    }
  };

  scrollToTop = () => {
    const scroller = this.scroll.getScroller();
    scroller.scrollTop = 0;
  };

  scrollToBottom = () => {
    const scroller = this.scroll.getScroller();
    scroller.scrollTop = scroller.scrollHeight;
  };

  scrollTo = (to) => {
    const scroller = this.scroll.getScroller();
    scroller.scrollTop = to;
  };

  getScrollValues = () => {
    const scroller = this.scroll.getScroller();
    return {
      clientHeight: scroller.clientHeight,
      scrollHeight: scroller.scrollHeight,
      scrollTop: scroller.scrollTop
    };
  };

  onScroll = () => {
    const { onScroll, scrollEvent } = this.props;
    const values = this.getScrollValues();
    if (onScroll) onScroll(values);
    if (scrollEvent) this.dispatchEvent(values);
  };

  dispatchEvent = (values) => {
    const { scrollEvent } = this.props;
    const event = createEvent(scrollEvent);
    event.values = values;
    document.dispatchEvent(event);
  };

  render() {
    const { classes, children } = this.props;
    return (
      <Baron
        ref={(scroll) => {
          this.scroll = scroll;
        }}
        clipperCls={classNames('clipper', classes.clipper)}
        scrollerCls={classNames('scroller', classes.scroller)}
        trackCls={classNames('track', classes.trackVertical)}
        barCls={classNames('bar', classes.thumbVertical)}
        onScroll={this.onScroll}
      >
        {children}
      </Baron>
    );
  }
}

export default withStyles(styles)(Scrollbar);