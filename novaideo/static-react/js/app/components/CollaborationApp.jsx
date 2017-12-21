import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

import Navbar from './Navbar';
import Footer from './Footer';
import { STYLE_CONST } from '../constants';

const styles = (theme) => {
  return {
    appBar: {
      transition: theme.transitions.create(['margin', 'width'], {
        easing: theme.transitions.easing.sharp,
        duration: STYLE_CONST.drawerDuration
      })
    },
    appBarShift: {
      [theme.breakpoints.up('md')]: {
        width: `calc(100% - ${STYLE_CONST.drawerChannelsWidth}px)`
      },
      transition: theme.transitions.create(['margin', 'width'], {
        easing: theme.transitions.easing.easeOut,
        duration: STYLE_CONST.drawerDuration
      })
    },
    'appBarShift-left': {
      [theme.breakpoints.up('md')]: {
        marginLeft: STYLE_CONST.drawerChannelsWidth
      }
    },
    main: {
      width: '100%',
      flexGrow: 1,
      paddingTop: 8,
      marginLeft: 0,
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.sharp,
        duration: STYLE_CONST.drawerDuration
      }),
      marginTop: 56,
      [theme.breakpoints.up('sm')]: {
        content: {
          marginTop: 64
        }
      }
    },
    app: {
      width: '100%'
    },
    appShift: {
      display: 'none',
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: STYLE_CONST.drawerDuration
      })
    },
    'appShift-left': {
      [theme.breakpoints.up('md')]: {
        marginLeft: STYLE_CONST.drawerChannelsWidth
      }
    }
  };
};

class CollaborationApp extends React.Component {
  render() {
    const { classes, channelsOpened, toggleChannels } = this.props;
    return (
      <div
        className={classNames(classes.app, {
          [classes.appShift]: channelsOpened,
          [classes['appShift-left']]: channelsOpened
        })}
      >
        <Navbar
          className={classNames(classes.appBar, {
            [classes.appBarShift]: channelsOpened,
            [classes['appBarShift-left']]: channelsOpened
          })}
          channelsOpened={channelsOpened}
          toggleChannels={toggleChannels}
        />
        <main className={classes.main}>
          <div className="app-child">
            {this.props.children}
          </div>
          <Footer />
        </main>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(CollaborationApp);