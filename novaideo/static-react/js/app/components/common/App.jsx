import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

import { STYLE_CONST } from '../../constants';

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
        width: `calc(100% - ${STYLE_CONST.drawerWidth}px)`
      },
      transition: theme.transitions.create(['margin', 'width'], {
        easing: theme.transitions.easing.easeOut,
        duration: STYLE_CONST.drawerDuration
      })
    },
    'appBarShift-left': {
      [theme.breakpoints.up('md')]: {
        marginLeft: STYLE_CONST.drawerWidth
      }
    },
    main: {
      width: '100%',
      flexGrow: 1,
      paddingTop: 8,
      marginLeft: 0,
      fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif',
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
      width: '100%',
      display: 'none'
    },
    appShift: {
      display: 'block',
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: STYLE_CONST.drawerDuration
      })
    },
    'appShift-left': {
      [theme.breakpoints.up('md')]: {
        marginLeft: STYLE_CONST.drawerWidth
      }
    }
  };
};

export const DumbApp = ({ data, classes, Navbar, active, left, children }) => {
  return (
    <div
      className={classNames(classes.app, {
        [classes.appShift]: active,
        [classes['appShift-left']]: left
      })}
    >
      <Navbar
        className={classNames(classes.appBar, {
          [classes.appBarShift]: left,
          [classes['appBarShift-left']]: left
        })}
        data={data}
      />
      <main className={classes.main}>
        <div className="app-child">
          {children}
        </div>
      </main>
    </div>
  );
};

export default withStyles(styles)(DumbApp);