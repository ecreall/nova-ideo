import React from 'react';
import { withStyles } from 'material-ui/styles';
import Dialog from 'material-ui/Dialog';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import IconButton from 'material-ui/IconButton';
import Typography from 'material-ui/Typography';
import CloseIcon from 'material-ui-icons/Close';
import Slide from 'material-ui/transitions/Slide';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%'
  },
  appBar: {
    position: 'relative',
    backgroundColor: '#fff',
    boxShadow: '0 1px 0 rgba(0,0,0,.1)'
  },
  paper: {
    backgroundColor: '#f3f3f3'
  },
  flex: {
    flex: 1
  }
};

function Transition(props) {
  return <Slide direction="up" {...props} />;
}

class CommonDialog extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      entered: false
    };
  }

  componentDidMount() {
    setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
    }, 0);
  }

  onEntered = () => {
    this.setState({ entered: true });
  };

  onClose = () => {
    this.setState({ entered: false }, this.props.onClose);
  };

  render() {
    const { appBar, children, classes, open, fullScreen, transition } = this.props;
    return (
      <Dialog
        classes={{ paper: classes.paper }}
        onEntered={this.onEntered}
        fullScreen={fullScreen}
        open={open}
        onClose={this.onClose}
        transition={transition && Transition}
      >
        {appBar &&
          <AppBar className={classes.appBar}>
            <Toolbar>
              <Typography type="title" color="primary" className={classes.flex}>
                {appBar}
              </Typography>
              <IconButton color="primary" onClick={this.onClose} aria-label="Close">
                <CloseIcon />
              </IconButton>
            </Toolbar>
          </AppBar>}
        {this.state.entered &&
          <div className={classes.container}>
            {children}
          </div>}
      </Dialog>
    );
  }
}

export default withStyles(styles)(CommonDialog);