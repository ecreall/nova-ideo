import React from 'react';
import { withStyles } from 'material-ui/styles';
import Drawer from 'material-ui/Drawer';
import classNames from 'classnames';
import Hidden from 'material-ui/Hidden';
import { connect } from 'react-redux';

import { updateApp } from '../../actions/actions';
import { STYLE_CONST } from '../../constants';
import Channels from './Channels';

const styles = (theme) => {
  return {
    container: {
      display: 'flex',
      flexDirection: 'column',
      height: '100%'
    },
    icon: { color: theme.palette.primary['50'] },
    drawerHeader: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'flex-end',
      padding: '0 8px',
      ...theme.mixins.toolbar
    },
    drawerPaper: {
      position: 'fixed',
      height: '100%',
      backgroundColor: theme.palette.primary['500'],
      overflow: 'hidden'
    },
    temporaryDrawerPaper: {
      width: 220,
      backgroundColor: theme.palette.primary['500'],
      [theme.breakpoints.up('md')]: {
        width: STYLE_CONST.drawerChannelsWidth,
        position: 'relative',
        height: '100%'
      }
    }
  };
};

function ChannelsDrawerContent({ classes }) {
  return (
    <div className={classes.container}>
      <div className={classes.drawerHeader} />
      <Channels />
    </div>
  );
}

class ChannelsDrawer extends React.Component {
  componentDidUpdate() {
    this.dispatchResize();
  }

  dispatchResize = () => {
    const event = document.createEvent('HTMLEvents');
    event.initEvent('resize', true, true);
    document.dispatchEvent(event);
  };

  render() {
    const { classes, theme, toggleChannelsDrawer, channelsDrawer } = this.props;
    return [
      <Hidden mdUp>
        <Drawer
          type="temporary"
          anchor={theme.direction === 'rtl' ? 'right' : 'left'}
          open={channelsDrawer}
          classes={{
            paper: classes.temporaryDrawerPaper
          }}
          onClose={() => {
            return toggleChannelsDrawer('chatApp', { drawer: false });
          }}
          ModalProps={{
            keepMounted: true // Better open performance on mobile.
          }}
        >
          <ChannelsDrawerContent classes={classes} />
        </Drawer>
      </Hidden>,
      <Hidden mdDown implementation="css">
        <Drawer
          type="persistent"
          classes={{
            paper: classNames(classes.drawerPaper)
          }}
          open={channelsDrawer}
          onClose={() => {
            return toggleChannelsDrawer('chatApp', { drawer: false });
          }}
        >
          <ChannelsDrawerContent classes={classes} />
        </Drawer>
      </Hidden>
    ];
  }
}

export const mapDispatchToProps = {
  toggleChannelsDrawer: updateApp
};

export const mapStateToProps = (state) => {
  return {
    channelsDrawer: state.apps.chatApp.drawer
  };
};
export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(ChannelsDrawer));