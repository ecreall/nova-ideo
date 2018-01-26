import React from 'react';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import ChatIcon from 'material-ui-icons/Chat';
import SpeakerNotesOff from 'material-ui-icons/SpeakerNotesOff';
import Drawer from 'material-ui/Drawer';
import { connect } from 'react-redux';

import { updateApp } from '../actions/actions';
import AppMenu from './AppMenu';
import AccountInformation from './AccountInformation';

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
  },
  userMenuContainer: {
    paddingLeft: 30,
    paddingRight: 30
  },
  accountAvatar: {
    width: 30,
    height: 30,
    borderRadius: 4
  }
};

class NavBar extends React.Component {
  state = {
    drawerMenu: false
  };

  toggleDrawer = (drawer, open) => {
    return () => {
      this.setState({
        [drawer]: open
      });
    };
  };

  render() {
    const { classes, className, toggleChannelsDrawer, channelsDrawer, site } = this.props;
    return (
      <div>
        <AppBar className={className} color="inherit">
          <Toolbar>
            <IconButton
              className={classes.menuButton}
              color="primary"
              aria-label="Menu"
              onClick={this.toggleDrawer('drawerMenu', true)}
            >
              <MenuIcon />
            </IconButton>
            <IconButton
              className={classes.menuButton}
              color="primary"
              aria-label="Menu"
              onClick={() => {
                return toggleChannelsDrawer('chatApp', { drawer: !channelsDrawer });
              }}
            >
              {channelsDrawer ? <SpeakerNotesOff /> : <ChatIcon />}
            </IconButton>
            <Typography type="title" color="primary" className={classes.flex}>
              {site.title}
            </Typography>
            <div className={classes.userMenuContainer}>
              <AccountInformation
                onlyIcon
                classes={{
                  avatar: classes.accountAvatar
                }}
              />
            </div>
          </Toolbar>
        </AppBar>
        <Drawer open={this.state.drawerMenu} onClose={this.toggleDrawer('drawerMenu', false)}>
          <div
            tabIndex={0}
            role="button"
            onClick={this.toggleDrawer('drawerMenu', false)}
            onKeyDown={this.toggleDrawer('drawerMenu', false)}
          >
            <AppMenu />
          </div>
        </Drawer>
      </div>
    );
  }
}

export const mapDispatchToProps = {
  toggleChannelsDrawer: updateApp
};

export const mapStateToProps = (state) => {
  return {
    channelsDrawer: state.apps.chatApp.drawer,
    site: state.globalProps.siteConf
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(NavBar));