import React from 'react';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';

import Drawer from './components/Drawer';
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

  render() {
    const { data, classes, children, channelOpen, drawerOpen, channel } = this.props;
    if (data.loading) return null;
    return (
      <div className={classes.root}>
        <div className={classes.appFrame}>
          <CollaborationApp active={!channelOpen} left={drawerOpen || channelOpen}>
            {children}
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