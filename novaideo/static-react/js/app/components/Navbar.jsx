import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import KeyboardArrowLeftIcon from 'material-ui-icons/KeyboardArrowLeft';
import KeyboardArrowRightIcon from 'material-ui-icons/KeyboardArrowRight';
import Drawer from 'material-ui/Drawer';
import { connect } from 'react-redux';

import { updateApp } from '../actions/actions';
import AppMenu from './AppMenu';
import AccountInformation from './user/AccountInformation';
import UserMenu from './user/UserMenu';

const styles = {
  root: {
    width: '100%'
  },
  flex: {
    flex: 1
  },
  appBar: {
    boxShadow: '0 1px 0 rgba(0,0,0,.1)'
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
    borderRadius: 4,
    cursor: 'pointer'
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
    const { classes, className, toggleDrawer, drawer, site } = this.props;
    return (
      <div>
        <AppBar className={classNames(className, classes.appBar)} color="inherit">
          <Toolbar>
            <IconButton
              className={classes.menuButton}
              color="primary"
              aria-label="Menu"
              onClick={() => {
                return toggleDrawer('drawer', { open: !drawer });
              }}
            >
              {drawer ? <KeyboardArrowLeftIcon /> : <KeyboardArrowRightIcon />}
            </IconButton>
            <IconButton
              className={classes.menuButton}
              color="primary"
              aria-label="Menu"
              onClick={this.toggleDrawer('drawerMenu', true)}
            >
              <MenuIcon />
            </IconButton>
            <Typography type="title" color="primary" className={classes.flex}>
              {!drawer && site.title}
            </Typography>
            {!drawer &&
              <div className={classes.userMenuContainer}>
                <UserMenu
                  activator={
                    <AccountInformation
                      onlyIcon
                      classes={{
                        avatar: classes.accountAvatar
                      }}
                    />
                  }
                />
              </div>}
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
  toggleDrawer: updateApp
};

export const mapStateToProps = (state) => {
  return {
    drawer: state.apps.drawer.open,
    site: state.globalProps.site
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(NavBar));