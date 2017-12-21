import React from 'react';
import { withStyles } from 'material-ui/styles';
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

class App extends React.Component {
  state = {
    drawerChannels: false
  };

  toggleDrawer = (drawer, open) => {
    return () => {
      this.setState({
        [drawer]: open
      });
    };
  };

  toggleChannels = (open) => {
    return this.toggleDrawer('drawerChannels', open);
  };

  render() {
    const { classes } = this.props;
    const open = this.state.drawerChannels;
    return (
      <div className={classes.root}>
        <div className={classes.appFrame}>
          <CollaborationApp channelsOpened={open} toggleChannels={this.toggleChannels}>
            {this.props.children}
          </CollaborationApp>
          <ChatApp channelsOpened={open} toggleChannels={this.toggleChannels} />
          <ChannelsDrawer channelsOpened={open} toggleChannels={this.toggleChannels} />
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(App);