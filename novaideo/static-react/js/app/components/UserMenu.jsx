import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import KeyboardArrowDownIcon from 'material-ui-icons/KeyboardArrowDown';
import Avatar from 'material-ui/Avatar';

import { DEFAULT_LOGO } from '../constants';
import AccountInformation from './AccountInformation';
import { MenuList, Menu } from './common/menu';
import ShortcutsManager from './common/ShortcutsManager';

const styles = (theme) => {
  return {
    drawerHeader: {
      padding: '0 15px',
      paddingBottom: 2,
      cursor: 'pointer',
      ...theme.mixins.toolbar,
      '&:hover': {
        backgroundColor: 'rgba(0, 0, 0, 0.12)',
        '& .account-title-text': {
          color: 'white'
        },
        '& .arrow': {
          color: 'white'
        }
      }
    },
    drawerHeaderActive: {
      backgroundColor: 'rgba(0, 0, 0, 0.12)',
      '& .account-title-text': {
        color: 'white'
      },
      '& .arrow': {
        color: 'white'
      }
    },
    siteInfo: {
      display: 'flex',
      alignItems: 'center',
      paddingTop: 9,
      marginBottom: 5
    },
    siteTitle: {
      display: 'block',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      fontSize: 17,
      lineHeight: 1.375,
      fontWeight: 900,
      color: '#fff'
    },
    arrow: {
      color: theme.palette.primary.light,
      width: 17,
      height: 17
    },
    sectionHeaderTitle: {
      display: 'flex',
      position: 'relative',
      justifyContent: 'flex-start'
    },
    sectionHeaderTitleContainer: {
      paddingLeft: 7
    },
    sectionHeaderTitleText: {
      color: '#2c2d30',
      fontSize: 18,
      fontWeight: 900
    },
    sectionHeaderAddon: {
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      textDecoration: 'none',
      color: '#a0a0a2',
      fontWeight: 500,
      fontSize: 15
    },
    avatar: {
      width: 36,
      height: 36,
      borderRadius: 4
    }
  };
};

class UserMenu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      menu: false
    };
    this.popper = null;
    this.anchor = null;
  }

  handleOpen = (event) => {
    if (this.popper) {
      this.popper.open(event, this.anchor);
    }
    return false;
  };

  onMenuOpen = () => {
    this.setState({ menu: true });
  };

  onMenuClose = () => {
    this.setState({ menu: false });
  };

  userSectionHeader = () => {
    const { classes, account } = this.props;
    const picture = account.picture;
    return (
      <div className={classes.sectionHeaderTitle}>
        <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : ''} />
        <div className={classes.sectionHeaderTitleContainer}>
          <div className={classes.sectionHeaderTitleText}>
            {account.title}
          </div>
        </div>
      </div>
    );
  };

  siteSectionHeader = () => {
    const { classes, site } = this.props;
    const picture = site.logo;
    return (
      <div className={classes.sectionHeaderTitle}>
        <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : DEFAULT_LOGO} />
        <div className={classes.sectionHeaderTitleContainer}>
          <div className={classes.sectionHeaderTitleText}>
            {site.title}
          </div>
          <div className={classes.sectionHeaderAddon}>
            {window.location.host}
          </div>
        </div>
      </div>
    );
  };

  render() {
    const { site, classes, theme, activator } = this.props;
    const { menu } = this.state;
    return (
      <ShortcutsManager domain="APP" shortcuts={{ OPEN_USER_MENU: this.handleOpen }}>
        <Menu
          initRef={(popper) => {
            this.popper = popper;
          }}
          id="user-menu"
          onOpen={this.onMenuOpen}
          onClose={this.onMenuClose}
          activator={
            <div
              ref={(anchor) => {
                this.anchor = anchor;
              }}
            >
              {activator ||
                <div className={classNames(classes.drawerHeader, { [classes.drawerHeaderActive]: menu })}>
                  <div className={classes.siteInfo}>
                    <div className={classes.siteTitle}>
                      {site.title}
                    </div>
                    <KeyboardArrowDownIcon className={classNames('arrow', classes.arrow)} />
                  </div>
                  <AccountInformation color={theme.palette.primary.light} />
                </div>}
            </div>
          }
        >
          <MenuList
            header={this.userSectionHeader()}
            fields={[
              {
                title: 'Une action importante'
              },
              {
                title: 'Un autre action importante'
              }
            ]}
          />
          <MenuList
            header={this.siteSectionHeader()}
            fields={[
              {
                title: 'Une action importante'
              },
              {
                title: 'Un autre action importante'
              }
            ]}
          />
        </Menu>
      </ShortcutsManager>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    site: state.globalProps.site,
    account: state.globalProps.account
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(UserMenu));