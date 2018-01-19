import React from 'react';
import Icon from 'material-ui/Icon';
import Dialog, { DialogContent, DialogContentText, DialogTitle } from 'material-ui/Dialog';
import Slide from 'material-ui/transitions/Slide';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';

function Transition(props) {
  return <Slide direction="up" {...props} />;
}

const styles = {
  circleContainer: {
    cursor: 'pointer'
  },
  circle: {
    color: 'gray',
    fontSize: 22
  },
  top: {
    color: '#f13b2d',
    textShadow: '0 0px 4px #f13b2d'
  },
  middle: {
    color: '#ef6e18',
    textShadow: '0 0px 4px #ef6e18'
  },
  bottom: {
    color: '#4eaf4e',
    textShadow: '0 0px 4px #4eaf4e'
  }
};

class Examination extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: false
    };
  }
  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  render() {
    const { value, title, message, classes } = this.props;
    return [
      <div className={classes.circleContainer} onClick={this.handleClickOpen}>
        <Icon className={classNames(classes.circle, classes[value], 'mdi-set mdi-checkbox-blank-circle')} />
      </div>,
      <Dialog
        open={this.state.open}
        transition={Transition}
        onClose={this.handleClose}
        aria-labelledby="alert-dialog-slide-title"
        aria-describedby="alert-dialog-slide-description"
      >
        <DialogTitle id="alert-dialog-slide-title">
          {title}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-slide-description">
            {message}
          </DialogContentText>
        </DialogContent>
      </Dialog>
    ];
  }
}

export default withStyles(styles)(Examination);