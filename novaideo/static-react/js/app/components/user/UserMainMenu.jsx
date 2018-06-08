import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import Avatar from '@material-ui/core/Avatar';
import { Query } from 'react-apollo';

import Actions from '../../graphql/queries/Actions.graphql';
import { DEFAULT_LOGO } from '../../constants';
import AccountInformation from './AccountInformation';
import { MenuList, Menu } from '../common/menu';
import ShortcutsManager from '../common/ShortcutsManager';
import { getFields } from '../common/MenuMore';
import { filterActions, getActions } from '../../utils/processes';
import { ACTIONS } from '../../processes';
import UserProcessManager from './UserProcessManager';

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

export class DumbUserMainMenu extends React.Component {
  state = {
    menu: false
  };

  popper = null;

  anchor = null;

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
    const picture = account && account.picture;
    return (
      <div className={classes.sectionHeaderTitle}>
        <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : ''} />
        <div className={classes.sectionHeaderTitleContainer}>
          <div className={classes.sectionHeaderTitleText}>{account && account.title}</div>
        </div>
      </div>
    );
  };

  siteSectionHeader = () => {
    const { classes, site } = this.props;
    const picture = site && site.logo;
    return (
      <div className={classes.sectionHeaderTitle}>
        <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : DEFAULT_LOGO} />
        <div className={classes.sectionHeaderTitleContainer}>
          <div className={classes.sectionHeaderTitleText}>{site && site.title}</div>
          <div className={classes.sectionHeaderAddon}>{window.location.host}</div>
        </div>
      </div>
    );
  };

  close = (event, callback) => {
    this.popper.close(event, callback);
  };

  render() {
    const { account, rootActions, site, processManager, classes, theme, activator } = this.props;
    const { menu } = this.state;
    const siteActions = filterActions(rootActions, { tags: [ACTIONS.mainMenu, ACTIONS.site] });
    const siteFields = getFields(siteActions, processManager.execute, theme, { siteTitle: site.title });
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
              {activator || (
                <div className={classNames(classes.drawerHeader, { [classes.drawerHeaderActive]: menu })}>
                  <div className={classes.siteInfo}>
                    <div className={classes.siteTitle}>{site && site.title}</div>
                    <KeyboardArrowDownIcon className={classNames('arrow', classes.arrow)} />
                  </div>
                  {account && <AccountInformation color={theme.palette.primary.light} />}
                </div>
              )}
            </div>
          }
        >
          {account ? (
            <Query
              notifyOnNetworkStatusChange
              fetchPolicy="cache-and-network"
              query={Actions}
              variables={{
                context: account.oid,
                processIds: [],
                nodeIds: [],
                processTags: [],
                actionTags: [ACTIONS.mainMenu]
              }}
            >
              {(result) => {
                const data = result.data;
                if (!data.actions) return null;
                const userActions = getActions(
                  data.actions.edges.map((action) => {
                    return action.node;
                  })
                );
                const userFields = getFields(userActions, processManager.execute, theme);
                return <MenuList header={this.userSectionHeader()} fields={userFields} close={this.close} />;
              }}
            </Query>
          ) : null}
          <MenuList header={this.siteSectionHeader()} fields={siteFields} />
        </Menu>
      </ShortcutsManager>
    );
  }
}

function UserMainMenuWithProcessManager(props) {
  const { account, onActionClick } = props;
  return (
    <UserProcessManager person={account} onActionClick={onActionClick}>
      <DumbUserMainMenu {...props} />
    </UserProcessManager>
  );
}

export const mapStateToProps = (state) => {
  return {
    site: state.globalProps.site,
    rootActions: state.globalProps.rootActions,
    account: state.globalProps.account
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(UserMainMenuWithProcessManager));