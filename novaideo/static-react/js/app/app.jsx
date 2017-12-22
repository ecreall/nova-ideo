import React from 'react';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';

import ChannelsDrawer from './components/channels/ChannelsDrawer';
import CollaborationApp from './components/CollaborationApp';
import ChatApp from './components/ChatApp';

const styles = {
  root: {
    width: '100%',
    zIndex: 1,
    overflow: 'hidden'
  },
  appFrame: {
    position: 'relative',
    display: 'flex',
    width: '100%',
    height: '100%'
  }
};

function App({ classes, children, channelOpen, channelsDrawer, channel }) {
  return (
    <div className={classes.root}>
      <div className={classes.appFrame}>
        <CollaborationApp active={!channelOpen} left={channelsDrawer || channelOpen}>
          {children}
        </CollaborationApp>
        {channel && <ChatApp active={channelOpen} left={channelsDrawer || channelOpen} />}
        <ChannelsDrawer />
      </div>
    </div>
  );
}

export const mapStateToProps = (state) => {
  return {
    channelOpen: state.apps.chatApp.open,
    channelsDrawer: state.apps.chatApp.drawer,
    channel: state.apps.chatApp.channel
  };
};

export default withStyles(styles)(connect(mapStateToProps)(App));