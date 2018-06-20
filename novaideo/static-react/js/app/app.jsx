import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';

import Drawer from './components/drawer/Drawer';
import CollaborationApp from './components/collaborationApp/CollaborationApp';
import ChatApp from './components/chatApp/ChatApp';
import Account from './graphql/queries/Account.graphql';
import { updateGlobalProps } from './actions/instanceActions';
import Home from './components/collaborationApp/Home';
import { setInputValue } from './utils/globalFunctions';

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
    const { data, site } = nextProps;
    this.props.updateGlobalProps({
      account: data.account
    });
    const accountId = data.account ? data.account.id : 'anonymous';
    setInputValue('execution-id', `${site.id}-${accountId}`);
  }

  render() {
    const { data, classes, children, channelOpen, drawerOpen, channel } = this.props;
    if (data.loading) return null;
    return (
      <div className={classes.root}>
        <div className={classes.appFrame}>
          <CollaborationApp active={!channelOpen} left={drawerOpen || channelOpen}>
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
    channel: state.apps.chatApp.channel,
    site: state.globalProps.site
  };
};

export const mapDispatchToProps = {
  updateGlobalProps: updateGlobalProps
};

export default withStyles(styles)(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(
    graphql(Account, {
      options: () => {
        return {
          fetchPolicy: 'cache-and-network'
        };
      }
    })(DumbApp)
  )
);