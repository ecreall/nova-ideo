import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';
import Drawer from 'material-ui/Drawer';
import classNames from 'classnames';
import Hidden from 'material-ui/Hidden';
import IconButton from 'material-ui/IconButton';
import ChatIcon from 'material-ui-icons/Chat';
import SpeakerNotesOff from 'material-ui-icons/SpeakerNotesOff';
import { Slide } from 'material-ui/transitions';

import { STYLE_CONST } from '../constants';
import ChannelsDrawer from './channels/ChannelsDrawer';
import UserMenu from './user/UserMenu';
import UserDrawer from './user/UserDrawer';
import { updateApp, closeDrawer } from '../actions/actions';

const styles = (theme) => {
  return {
    container: {
      display: 'flex',
      flexDirection: 'column',
      height: '100%'
    },
    icon: { color: theme.palette.primary['50'] },
    drawerPaper: {
      position: 'fixed',
      height: '100%',
      backgroundColor: theme.palette.primary['500'],
      overflow: 'hidden',
      maxWidth: STYLE_CONST.drawerWidth
    },
    temporaryDrawerPaper: {
      width: STYLE_CONST.drawerWidth,
      backgroundColor: theme.palette.primary['500'],
      [theme.breakpoints.up('md')]: {
        width: STYLE_CONST.drawerWidth,
        position: 'relative',
        height: '100%'
      }
    },
    switchButton: {
      position: 'absolute',
      right: 0,
      color: 'white',
      opacity: 0.7,
      '&:hover': {
        opacity: 1
      }
    },
    drawersContainer: {
      display: 'flex',
      height: '100%'
    },
    userDrawer: {
      height: '100%',
      transform: 'inherit'
    },
    userDrawerOpen: {
      transform: `translate3d(-${STYLE_CONST.drawerWidth}px, 0px, 0px) !important`,
      transition: 'transform 225ms cubic-bezier(0, 0, 0.2, 1) 0ms'
    },
    channelsDrawer: {
      height: '100%'
    }
  };
};

function DrawerContent({ drawerApp, switchDrawer, classes }) {
  const isChatApp = drawerApp === 'chatApp';
  return (
    <div className={classes.container}>
      <IconButton
        className={classes.switchButton}
        color="primary"
        aria-label="Menu"
        onClick={() => {
          return switchDrawer('drawer', { app: isChatApp ? undefined : 'chatApp' });
        }}
      >
        {isChatApp ? <SpeakerNotesOff /> : <ChatIcon />}
      </IconButton>
      <UserMenu />
      <div className={classes.drawersContainer}>
        <Slide in={isChatApp} direction="right">
          <div className={classes.channelsDrawer}>
            <ChannelsDrawer />
          </div>
        </Slide>
        <Slide in={!isChatApp} direction="left">
          <div className={classNames(classes.userDrawer, { [classes.userDrawerOpen]: !isChatApp })}>
            <UserDrawer />
          </div>
        </Slide>
      </div>
    </div>
  );
}

class AppDrawer extends React.Component {
  componentDidUpdate() {
    this.dispatchResize();
  }

  dispatchResize = () => {
    const event = document.createEvent('HTMLEvents');
    event.initEvent('resize', true, true);
    document.dispatchEvent(event);
  };

  render() {
    const { classes, theme, drawerOpen, drawerApp, switchDrawer } = this.props;
    return [
      <Hidden mdUp>
        <Drawer
          type="temporary"
          anchor={theme.direction === 'rtl' ? 'right' : 'left'}
          open={drawerOpen}
          classes={{
            paper: classes.temporaryDrawerPaper
          }}
          onClose={() => {
            this.props.closeDrawer();
          }}
          ModalProps={{
            keepMounted: true // Better open performance on mobile.
          }}
        >
          <DrawerContent classes={classes} drawerApp={drawerApp} switchDrawer={switchDrawer} />
        </Drawer>
      </Hidden>,
      <Hidden mdDown implementation="css">
        <Drawer
          type="persistent"
          classes={{
            paper: classNames(classes.drawerPaper)
          }}
          open={drawerOpen}
          onClose={() => {
            this.props.closeDrawer();
          }}
        >
          <DrawerContent classes={classes} drawerApp={drawerApp} switchDrawer={switchDrawer} />
        </Drawer>
      </Hidden>
    ];
  }
}

export const mapDispatchToProps = {
  closeDrawer: closeDrawer,
  switchDrawer: updateApp
};

export const mapStateToProps = (state) => {
  return {
    drawerOpen: state.apps.drawer.open,
    drawerApp: state.apps.drawer.app
  };
};
export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(AppDrawer));