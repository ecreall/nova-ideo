import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import KeyboardArrowLeftIcon from 'material-ui-icons/KeyboardArrowLeft';
import KeyboardArrowRightIcon from 'material-ui-icons/KeyboardArrowRight';
import { connect } from 'react-redux';

import { toggleDrawer } from '../../actions/collaborationAppActions';
import AccountInformation from '../user/AccountInformation';
import UserMenu from '../user/UserMenu';
import Search from '../forms/Search';

const styles = {
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
  },
  menuContainer: {
    display: 'flex',
    alignItems: 'center',
    height: 34,
    margin: '2px 0 0',
    padding: '0 10px 0 0',
    transition: 'width .15s ease-out 0s',
    width: 360,
    '&:focus-within': {
      width: 437
    },
    '@media (max-width:1440px)': {
      width: 315,
      '&:focus-within': {
        width: 387
      }
    },
    '@media (max-width:1366px)': {
      width: 260,
      '&:focus-within': {
        width: 337
      }
    },
    '@media (max-width:1279px)': {
      width: 245,
      '&:focus-within': {
        width: 312
      }
    },
    '@media (max-width:1070px)': {
      width: 225,
      '&:focus-within': {
        width: 282
      }
    },
    '@media (max-width:860px)': {
      width: 195,
      '&:focus-within': {
        width: 257
      }
    }
  }
};

class NavBar extends React.Component {
  handelSearch = () => {
    // todo
  };

  render() {
    const { classes, className, drawer, site } = this.props;
    return (
      <div>
        <AppBar className={classNames(className, classes.appBar)} color="inherit">
          <Toolbar>
            <IconButton className={classes.menuButton} color="primary" aria-label="Menu" onClick={this.props.toggleDrawer}>
              {drawer ? <KeyboardArrowLeftIcon /> : <KeyboardArrowRightIcon />}
            </IconButton>
            <Typography type="title" color="primary" className={classes.flex}>
              {!drawer && site.title}
            </Typography>
            <div className={classes.menuContainer}>
              <Search
                form={'globalSearch'}
                key={'globalSearch'}
                onSearch={this.handelSearch}
                onCancel={this.handleSearchCancel}
                title={'Search'}
              />
            </div>
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
      </div>
    );
  }
}

export const mapDispatchToProps = {
  toggleDrawer: toggleDrawer
};

export const mapStateToProps = (state) => {
  return {
    drawer: state.apps.drawer.open,
    site: state.globalProps.site
  };
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(NavBar));