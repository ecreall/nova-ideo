/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { Translate } from 'react-redux-i18n';
import Grow from 'material-ui/transitions/Grow';
import { connect } from 'react-redux';

import { search } from '../../actions/collaborationAppActions';
import { getFormattedDate } from '../../utils/globalFunctions';
import AllignedActions from '../common/AllignedActions';
import { getActions } from '../../utils/processes';
import { ACTIONS } from '../../processes';
import UserMenu from './UserMenu';
import UserAvatar from './UserAvatar';
import UserTitle from './UserTitle';
import Search from '../forms/Search';

const styles = (theme) => {
  return {
    header: {
      display: 'flex',
      flexDirection: 'column',
      margin: '0 10px',
      position: 'relative'
    },
    headerTitle: {
      fontSize: 15,
      color: '#2c2d30',
      fontWeight: 900,
      lineHeight: 'normal'
    },
    titleContainer: {
      display: 'flex'
    },
    headerAddOn: {
      color: '#999999ff',
      fontSize: 12,
      lineHeight: 'normal'
    },
    appBarContainer: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    appbarActions: {
      display: 'flex',
      marginRight: 10
    },
    menu: {
      position: 'relative',
      border: 'none',
      boxShadow: 'none',
      marginRight: 5
    },
    menuButton: {
      color: '#2c2d30'
    },
    menuAction: {
      borderRight: 'none'
    },
    publishAction: {
      marginRight: '20px !important',
      minWidth: 'auto',
      minHeight: 'auto',
      padding: '5px 10px'
    },
    menuContainer: {
      display: 'flex',
      alignItems: 'center',
      margin: '2px 0 0',
      fontWeight: 100
    },
    search: {
      height: 34,
      transition: 'width .15s ease-out 0s',
      minWidth: 360,
      '&:focus-within': {
        minWidth: 437
      },
      '@media (max-width:1440px)': {
        minWidth: 315,
        '&:focus-within': {
          minWidth: 387
        }
      },
      '@media (max-width:1366px)': {
        minWidth: 260,
        '&:focus-within': {
          minWidth: 337
        }
      },
      '@media (max-width:1279px)': {
        minWidth: 245,
        '&:focus-within': {
          minWidth: 312
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
    },
    searchContainer: {
      paddingLeft: 5
    },
    actionsContainer: {
      height: 45,
      width: 'auto',
      paddingRight: 0,
      paddingLeft: 0,
      marginLeft: 10
    },
    actionsText: {
      color: '#2c2d30',
      marginRight: 5,
      fontSize: 14,
      fontWeight: 400,
      '&:hover': {
        color: theme.palette.info['700']
      }
    },
    actionsIcon: {
      fontWeight: 100,
      fontSize: '20px !important',
      marginRight: 5,
      marginTop: -2,
      height: 20,
      width: 20
    },
    userDataContainer: {
      display: 'flex',
      alignItems: 'center'
    }
  };
};

class UserAppBar extends React.Component {
  state = {
    userDataVisible: false
  };

  componentDidMount() {
    const { initRef } = this.props;
    if (initRef) {
      initRef(this);
    }
  }

  handelSearch = (filter) => {
    const { person } = this.props;
    this.props.search(`${person.id}-search`, filter.text);
  };

  handleSearchCancel = () => {
    const { person } = this.props;
    this.props.search(`${person.id}-search`, '');
  };

  open = () => {
    this.setState({ userDataVisible: true });
  };

  close = () => {
    this.setState({ userDataVisible: false });
  };

  render() {
    const { person, processManager, classes } = this.props;
    const { userDataVisible } = this.state;
    const authorPicture = person.picture;
    const isAnonymous = person.isAnonymous;
    const communicationActions = getActions(person.actions, { tags: ACTIONS.communication });
    const fCreatedAt = getFormattedDate(person.createdAt, 'date.format');
    return (
      <div className={classes.appBarContainer}>
        <Grow in={userDataVisible} timeout={100}>
          <div className={classes.userDataContainer}>
            <div className={classes.titleContainer}>
              <UserAvatar isAnonymous={isAnonymous} picture={authorPicture} title={person.title} />
              <div className={classes.header}>
                <UserTitle node={person} classes={{ title: classes.headerTitle }} />
                <span className={classes.headerAddOn}>
                  {person.function || <Translate value="user.subscribed" date={fCreatedAt} />}
                </span>
              </div>
            </div>
            {communicationActions.length > 0
              ? <AllignedActions
                type="button"
                actions={communicationActions}
                onActionClick={processManager.execute}
                overlayPosition="bottom"
                classes={{
                  actionsContainer: classes.actionsContainer,
                  actionsText: classes.actionsText,
                  actionsIcon: classes.actionsIcon
                }}
              />
              : null}
          </div>
        </Grow>
        <div className={classes.appbarActions}>
          <div className={classes.menuContainer}>
            <div className={classes.search}>
              <Search
                liveSearch
                form={`${person.id}-search`}
                key={`${person.id}-search`}
                onSearch={this.handelSearch}
                onCancel={this.handleSearchCancel}
                title={<Translate value="user.search" name={person.title} />}
                classes={{ container: classes.searchContainer }}
              />
            </div>
          </div>
          <UserMenu
            open
            overlayPosition="bottom"
            user={person}
            onActionClick={processManager.execute}
            classes={{ container: classes.menu, button: classes.menuButton, action: classes.menuAction }}
          />
        </div>
      </div>
    );
  }
}

export const mapDispatchToProps = {
  search: search
};

export default withStyles(styles, { withTheme: true })(connect(null, mapDispatchToProps)(UserAppBar));