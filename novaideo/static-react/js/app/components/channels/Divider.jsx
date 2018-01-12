/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

const styles = {
  divider: {
    position: 'relative',
    height: 1,
    backgroundColor: '#e6e6e6',
    margin: 10
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
    right: '50%',
    backgroundColor: 'white',
    top: -13,
    fontSize: '0.9rem',
    fontWeight: 'bold',
    color: '#2c2d30',
    cursor: 'default',
    textAlign: 'center',
    padding: 5,
    width: 130
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
  }
};

class Divider extends React.Component {
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
    document.addEventListener(this.props.eventId, this.handleScroll);
    document.addEventListener('resize', this.handleResize);
  }

  componentWillUnmount() {
    document.removeEventListener(this.props.eventId, this.handleScroll);
    document.removeEventListener('resize', this.handleResize);
  }

  handleScroll = () => {
    if (this.container && this.message) {
      const top = this.container.getBoundingClientRect().top;
      const { shift, fixedTop } = this.props;
      const left = this.message.offsetLeft + shift;
      if (!this.state.fixed && top < fixedTop) {
        this.setState({ fixed: true, left: left });
      } else if (this.state.fixed && top >= fixedTop + 10) {
        this.setState({ fixed: false });
      }
    }
  };

  handleResize = () => {
    if (this.container && this.message) {
      const { shift } = this.props;
      const left = this.message.offsetLeft + shift;
      if (this.state.fixed && this.state.left !== left) {
        this.setState({ left: left });
      }
    }
  };

  render() {
    const { index, message, alert, alertMessage, classes } = this.props;
    return (
      <div
        ref={(container) => {
          this.container = container;
        }}
        className={classNames(classes.divider, {
          [classes.dividerAlert]: alert,
          [classes.dividerFixed]: this.state.fixed
        })}
      >
        {alert &&
          <div className={classes.alert}>
            {alertMessage}
          </div>}
        {message &&
          <div
            ref={(messageContainer) => {
              this.message = messageContainer;
            }}
            style={this.state.fixed ? { left: this.state.left, zIndex: 3000 - index } : {}}
            className={classNames(classes.message, {
              [classes.messageFixed]: this.state.fixed
            })}
          >
            {message}
          </div>}
      </div>
    );
  }
}

export default withStyles(styles)(Divider);