/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import ReactDOM from 'react-dom';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import Grow from 'material-ui/transitions/Grow';
import Paper from 'material-ui/Paper';
import { Manager, Target, Popper as PopperBase } from 'react-popper';
import ClickAwayListener from 'material-ui/utils/ClickAwayListener';

const popperRoot = document.getElementById('menu-root');

const styles = {
  popper: {
    zIndex: 3000,
    '& .menu-section:last-child': {
      border: 'none'
    }
  },
  popperClose: {
    pointerEvents: 'none'
  },
  paper: {
    borderRadius: 6,
    width: 300,
    border: '1px solid rgba(0,0,0,.15)',
    maxHeight: 'calc(100vh - 99px)',
    overflowY: 'auto',
    overflowX: 'hidden'
  }
};

class Popper extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      popper: false
    };
    this.popper = document.createElement('div');
  }

  componentDidMount() {
    popperRoot.appendChild(this.popper);
    const { initRef } = this.props;
    if (initRef) {
      initRef(this);
    }
  }

  componentWillUnmount() {
    popperRoot.removeChild(this.popper);
  }

  openPopper = () => {
    const { onOpen } = this.props;
    this.setState({ popper: true }, () => {
      if (onOpen) {
        onOpen();
      }
    });
  };

  closePopper = (event, callback) => {
    const { onClose } = this.props;
    this.setState({ popper: false }, () => {
      if (callback) callback();
      if (onClose) onClose();
    });
  };

  render() {
    const { id, activator, classes } = this.props;
    const { popper } = this.state;
    const children = React.Children.map(this.props.children, (child) => {
      return React.cloneElement(child, {
        open: this.openPopper,
        close: this.closePopper
      });
    });
    return (
      <Manager
        className={classNames(classes.root, {
          [classes.rootOpen]: popper
        })}
      >
        <Target onClick={this.openPopper}>
          {activator}
        </Target>
        {ReactDOM.createPortal(
          <PopperBase
            placement="top-start"
            eventsEnabled={popper}
            className={classNames(classes.popper, { [classes.popperClose]: !popper })}
          >
            <ClickAwayListener onClickAway={this.closePopper}>
              <Grow in={popper} id={id} style={{ transformOrigin: '0 0 0' }}>
                <Paper elevation={6} className={classes.paper}>
                  {children}
                </Paper>
              </Grow>
            </ClickAwayListener>
          </PopperBase>,
          this.popper
        )}
      </Manager>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Popper);