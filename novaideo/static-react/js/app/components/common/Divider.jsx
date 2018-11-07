/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';

const styles = {
  divider: {
    position: 'relative',
    minHeight: 1,
    backgroundColor: '#e6e6e6',
    margin: '15px 0'
  },
  dividerFixed: {
    backgroundColor: 'transparent !important'
  },
  messageFixed: {
    top: '54px !important',
    position: 'fixed !important',
    zIndex: '1200',
    right: 0
  },
  message: {
    position: 'absolute',
    right: 'calc(50% - 69px)', // 130/2
    backgroundColor: 'white',
    top: -13,
    fontSize: 13,
    fontWeight: 'bold',
    color: '#2c2d30',
    cursor: 'default',
    textAlign: 'center',
    padding: 5,
    width: 130,
    borderRadius: 3,
    zIndex: 1
  },
  dividerAlert: {
    backgroundColor: '#d72b3f99'
  },
  alert: {
    position: 'absolute',
    right: 15,
    backgroundColor: 'white',
    top: -9,
    fontSize: 12,
    fontWeight: 'bold',
    color: '#d72b3f',
    cursor: 'default',
    textAlign: 'center',
    padding: '1px 5px',
    border: 'solid 1px #d72b3f',
    borderRadius: 6,
    boxShadow: '0 0px 5px #8080808a'
  },
  background: {
    minHeight: 1,
    backgroundColor: 'white',
    width: 130,
    margin: 'auto'
  }
};

export class DumbDivider extends React.Component {
  static defaultProps = {
    dynamic: true
  };

  state = {
    fixed: false,
    left: 0
  };

  componentDidMount() {
    const { eventId } = this.props;
    if (eventId) {
      document.addEventListener(eventId, this.updatePosition);
      document.addEventListener('resize', this.initializePosition);
      this.updatePosition();
    }
  }

  componentWillUnmount() {
    const { eventId } = this.props;
    if (eventId) {
      document.removeEventListener(eventId, this.updatePosition);
      document.removeEventListener('resize', this.initializePosition);
    }
  }

  container = null;

  message = null;

  updatePosition = () => {
    const { dynamic } = this.props;
    if (dynamic && this.container && this.message) {
      const { top } = this.container.getBoundingClientRect();
      const { shift, fixedTop, fullScreen } = this.props;
      const messageRecLeft = this.message.getBoundingClientRect().left;
      const messageOffsetLeft = this.message.offsetLeft;
      const left = (fullScreen ? messageRecLeft : messageOffsetLeft) + shift;
      const { fixed } = this.state;
      if (!fixed && top < fixedTop) {
        this.setState({ fixed: true, left: left });
      } else if (fixed && top >= fixedTop + 10) {
        this.setState({ fixed: false });
      }
    }
  };

  initializePosition = () => {
    const { dynamic } = this.props;
    if (dynamic && this.container && this.message) {
      const { fixed } = this.state;
      if (fixed) {
        this.setState({ fixed: false }, this.updatePosition);
      }
    }
  };

  getZIndex = () => {
    const { index, reverted } = this.props;
    const zIndex = 1100;
    return reverted ? zIndex + 200 - index : zIndex + index;
  };

  render() {
    const {
      message, alert, alertMessage, classes
    } = this.props;
    const { fixed, left } = this.state;
    const fixedStyle = fixed ? { left: left, zIndex: this.getZIndex() } : {};
    return (
      <div
        ref={(container) => {
          this.container = container;
        }}
        className={classNames(classes.divider, {
          [classes.dividerAlert]: alert,
          [classes.dividerFixed]: fixed
        })}
      >
        {alert && <div className={classes.alert}>{alertMessage}</div>}
        {message && (
          <React.Fragment>
            <div key="background" className={classes.background} />
            <div
              key="message"
              ref={(messageContainer) => {
                this.message = messageContainer;
              }}
              style={fixedStyle}
              className={classNames(classes.message, {
                [classes.messageFixed]: fixed
              })}
            >
              {message}
            </div>
          </React.Fragment>
        )}
      </div>
    );
  }
}

export default withStyles(styles)(DumbDivider);