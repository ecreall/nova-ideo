/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import Menu from 'material-ui/Menu';

const styles = {
  menu: {
    '& .menu-section:last-child': {
      border: 'none'
    }
  },
  menuPaper: {
    borderRadius: 6,
    width: 300,
    border: '1px solid rgba(0,0,0,.15)',
    maxHeight: 'calc(100vh - 99px)',
    overflowY: 'auto',
    overflowX: 'hidden'
  }
};

export class DumbMenuWithActivator extends React.Component {
  state = {
    anchorEl: null
  };

  componentDidMount() {
    const { initRef } = this.props;
    if (initRef) {
      initRef(this);
    }
  }

  open = (event, anchor) => {
    const anchorEl = anchor || event.currentTarget;
    const { onOpen } = this.props;
    this.setState({ anchorEl: anchorEl }, () => {
      if (onOpen) {
        onOpen();
      }
    });
  };

  close = (event, callback) => {
    const { onClose } = this.props;
    this.setState({ anchorEl: null }, () => {
      if (typeof callback === 'function') callback();
      if (onClose) onClose();
    });
  };

  render() {
    const { id, activator, keepMounted, anchorOrigin, classes } = this.props;
    const { anchorEl } = this.state;
    const children = React.Children.map(this.props.children, (child) => {
      return React.cloneElement(child, {
        open: this.open,
        close: this.close
      });
    });
    const open = Boolean(anchorEl);
    return [
      <div onClick={this.open}>
        {activator}
      </div>,
      <Menu
        transitionDuration={150}
        keepMounted={keepMounted}
        className={classes.menu}
        classes={{ paper: classes.menuPaper }}
        id={id}
        anchorEl={anchorEl}
        open={open}
        onClose={this.close}
        anchorOrigin={anchorOrigin}
      >
        {children}
      </Menu>
    ];
  }
}

export default withStyles(styles, { withTheme: true })(DumbMenuWithActivator);