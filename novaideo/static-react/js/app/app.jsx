import React from 'react';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { Shortcuts } from 'react-shortcuts';
import keydown from 'react-keydown';

import ChannelsDrawer from './components/channels/ChannelsDrawer';
import CollaborationApp from './components/CollaborationApp';
import ChatApp from './components/ChatApp';
import { accountQuery } from './graphql/queries';
import { updateGlobalProps } from './actions/actions';

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
  componentWillReceiveProps(nextProps) {
    const { data } = nextProps;
    this.props.updateGlobalProps({
      account: data.account
    });
  }

  shortcuts = (action, event) => {
    if (action) {
      const eventToDispatch = document.createEvent('HTMLEvents');
      eventToDispatch.initEvent(action, true, true);
      document.dispatchEvent(eventToDispatch);
      event.preventDefault();
    }
  };

  render() {
    const { data, classes, children, channelOpen, channelsDrawer, channel } = this.props;
    if (data.loading) return null;
    return (
      <Shortcuts global alwaysFireHandler name="APP" handler={this.shortcuts} className={classes.root}>
        <div className={classes.appFrame}>
          <CollaborationApp active={!channelOpen} left={channelsDrawer || channelOpen}>
            {children}
          </CollaborationApp>
          {channel && <ChatApp active={channelOpen} left={channelsDrawer || channelOpen} params={this.props.params} />}
          <ChannelsDrawer />
        </div>
      </Shortcuts>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    channelOpen: state.apps.chatApp.open,
    channelsDrawer: state.apps.chatApp.drawer,
    channel: state.apps.chatApp.channel
  };
};

export const mapDispatchToProps = {
  updateGlobalProps: updateGlobalProps
};

export default withStyles(styles)(
  connect(mapStateToProps, mapDispatchToProps)(
    graphql(accountQuery, {
      options: () => {
        return {
          fetchPolicy: 'cache-first'
        };
      }
    })(DumbApp)
  )
);