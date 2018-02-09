/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
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
    right: 0,
    backgroundColor: 'white',
    top: -13,
    fontSize: '0.9rem',
    fontWeight: 'bold',
    color: '#d72b3f',
    cursor: 'default',
    textAlign: 'center',
    padding: 5
  },
  background: {
    minHeight: 1,
    backgroundColor: 'white',
    width: 130,
    margin: 'auto'
  }
};

class Divider extends React.Component {
  static defaultProps = {
    style: {
      message: {},
      messageFixed: {}
    }
  };
  constructor(props) {
    super(props);
    this.container = null;
    this.message = null;
    this.state = {
      fixed: false,
      left: 0
    };
  }

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
      document.removeEventListener(this.props.eventId, this.updatePosition);
      document.removeEventListener('resize', this.initializePosition);
    }
  }

  updatePosition = () => {
    if (this.container && this.message) {
      const top = this.container.getBoundingClientRect().top;
      const { shift, fixedTop, fullScreen } = this.props;
      const messageRecLeft = this.message.getBoundingClientRect().left;
      const messageOffsetLeft = this.message.offsetLeft;
      const left = (fullScreen ? messageRecLeft : messageOffsetLeft) + shift;
      if (!this.state.fixed && top < fixedTop) {
        this.setState({ fixed: true, left: left });
      } else if (this.state.fixed && top >= fixedTop + 10) {
        this.setState({ fixed: false });
      }
    }
  };

  initializePosition = () => {
    if (this.container && this.message) {
      if (this.state.fixed) {
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
    const { message, alert, alertMessage, classes, style } = this.props;
    const fixedStyle = this.state.fixed ? { left: this.state.left, zIndex: this.getZIndex() } : {};
    return (
      <div
        ref={(container) => {
          this.container = container;
        }}
        style={style.divider}
        className={classNames(classes.divider, {
          [classes.dividerAlert]: alert,
          [classes.dividerFixed]: this.state.fixed
        })}
      >
        {alert &&
          <div style={style.alert} className={classes.alert}>
            {alertMessage}
          </div>}
        {message && [
          <div className={classes.background} />,
          <div
            ref={(messageContainer) => {
              this.message = messageContainer;
            }}
            style={{ ...fixedStyle, ...style.message, ...(this.state.fixed ? style.messageFixed : {}) }}
            className={classNames(classes.message, {
              [classes.messageFixed]: this.state.fixed
            })}
          >
            {message}
          </div>
        ]}
      </div>
    );
  }
}

export default withStyles(styles)(Divider);