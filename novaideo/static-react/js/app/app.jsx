import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';

import Drawer from './components/drawer/Drawer';
import CollaborationApp from './components/collaborationApp/CollaborationApp';
import ChatApp from './components/chatApp/ChatApp';
import { updateGlobalProps } from './actions/instanceActions';
import Home from './components/collaborationApp/Home';

const styles = {
  root: {
    width: '100%',
    zIndex: 1,
    overflow: 'hidden',
    outline: 'none'
  },
  appFrame: {
    position: 'relative',
    display: 'flex',
    width: '100%',
    height: '100%'
  }
};

class DumbApp extends React.Component {
  render() {
    const {
      classes, children, channelOpen, drawerOpen, channel
    } = this.props;
    return (
      <div className={classes.root}>
        <div className={classes.appFrame}>
          <CollaborationApp active={!channelOpen} left={drawerOpen}>
            {children}
            <Home />
          </CollaborationApp>
          {channel && <ChatApp active={channelOpen} left={drawerOpen || channelOpen} />}
          <Drawer />
        </div>
      </div>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    channelOpen: state.apps.chatApp.open,
    drawerOpen: state.apps.drawer.open,
    channel: state.apps.chatApp.channel
  };
};

export const mapDispatchToProps = {
  updateGlobalProps: updateGlobalProps
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(DumbApp));