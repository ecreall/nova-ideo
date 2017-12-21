import React from 'react';
import { withStyles } from 'material-ui/styles';
import ChevronLeftIcon from 'material-ui-icons/ChevronLeft';
import ChevronRightIcon from 'material-ui-icons/ChevronRight';
import IconButton from 'material-ui/IconButton';
import Drawer from 'material-ui/Drawer';
import classNames from 'classnames';
import Hidden from 'material-ui/Hidden';

import { STYLE_CONST } from '../../constants';
import Channels from './Channels';

const styles = (theme) => {
  return {
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
      backgroundColor: theme.palette.primary['500']
    },
    drawerPaperOpen: {
      zIndex: 1501
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

function ChannelsDrawerContent({ classes, theme, toggleChannels }) {
  return (
    <div>
      <div className={classes.drawerHeader}>
        <IconButton onClick={toggleChannels(false)}>
          {theme.direction === 'rtl'
            ? <ChevronRightIcon className={classes.icon} />
            : <ChevronLeftIcon className={classes.icon} />}
        </IconButton>
      </div>
      <Channels />
    </div>
  );
}

class ChannelsDrawer extends React.Component {
  render() {
    const { classes, theme, toggleChannels, channelsOpened } = this.props;
    return [
      <Hidden mdUp>
        <Drawer
          type="temporary"
          anchor={theme.direction === 'rtl' ? 'right' : 'left'}
          open={channelsOpened}
          classes={{
            paper: classes.temporaryDrawerPaper
          }}
          onClose={toggleChannels(false)}
          ModalProps={{
            keepMounted: true // Better open performance on mobile.
          }}
        >
          <ChannelsDrawerContent classes={classes} theme={theme} toggleChannels={toggleChannels} />
        </Drawer>
      </Hidden>,
      <Hidden mdDown implementation="css">
        <Drawer
          type="persistent"
          classes={{
            paper: classNames(classes.drawerPaper, {
              [classes.drawerPaperOpen]: channelsOpened
            })
          }}
          open={channelsOpened}
          onClose={toggleChannels(false)}
        >
          <ChannelsDrawerContent classes={classes} theme={theme} toggleChannels={toggleChannels} />
        </Drawer>
      </Hidden>
    ];
  }
}

export default withStyles(styles, { withTheme: true })(ChannelsDrawer);