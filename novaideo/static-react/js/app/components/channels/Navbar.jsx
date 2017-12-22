import React from 'react';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import CloseIcon from 'material-ui-icons/Close';
import { connect } from 'react-redux';

import { updateApp } from '../../actions/actions';

const styles = {
  root: {
    width: '100%'
  },
  flex: {
    flex: 1
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20
  }
};

class NavBar extends React.Component {
  render() {
    const { data, classes, className, updateChatApp } = this.props;
    const channel = data.channel;
    return (
      <div>
        <AppBar className={className} color="inherit">
          <Toolbar>
            <Typography type="title" color="inherit" className={classes.flex}>
              {channel && channel.title}
            </Typography>
            <IconButton
              className={classes.menuButton}
              color="primary"
              aria-label="Menu"
              onClick={() => {
                return updateChatApp('chatApp', { open: false });
              }}
            >
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}

export const mapDispatchToProps = {
  updateChatApp: updateApp
};

export const mapStateToProps = (state) => {
  return {
    channelsDrawer: state.apps.chatApp.drawer
  };
};
export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(NavBar));