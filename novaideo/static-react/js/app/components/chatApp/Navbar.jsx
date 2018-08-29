import React from 'react';
import classNames from 'classnames';
import { Translate, I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Icon from '@material-ui/core/Icon';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import InfoOutlineIcon from '@material-ui/icons/InfoOutline';
import CloseIcon from '@material-ui/icons/Close';
import { connect } from 'react-redux';
import CardActions from '@material-ui/core/CardActions';
import ChatIcon from '@material-ui/icons/Chat';
import Hidden from '@material-ui/core/Hidden';

import { updateChatAppRight, closeChatApp } from '../../actions/chatAppActions';
import { openDrawer } from '../../actions/collaborationAppActions';
import ShortcutsManager from '../common/ShortcutsManager';
import OverlaidTooltip from '../common/OverlaidTooltip';
import { goTo, get } from '../../utils/routeMap';
import { CONTENTS_IDS } from './chatAppRight';
import Search from '../forms/Search';
import { getFormId } from '../../utils/globalFunctions';

const styles = (theme) => {
  return {
    root: {
      width: '100%'
    },
    menuContainer: {
      display: 'flex',
      alignItems: 'center',
      margin: '2px 0 0'
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
    titleContainer: {
      flex: 1,
      color: '#2c2d30',
      fontSize: 18,
      fontWeight: 900
    },
    title: {
      marginBottom: 15
    },
    titleBackground: {
      color: '#afafaf !important'
    },
    icon: {
      color: '#2c2d30',
      fontWeight: '900 !important',
      fontSize: '16px !important'
    },
    infoIcon: {
      height: 25,
      width: 25
    },
    filesIcon: {
      fontSize: '17px !important'
    },
    membersIcon: {
      fontSize: '20px !important'
    },
    appBar: {
      boxShadow: '0 1px 0 rgba(0,0,0,.1)'
    },
    menuButton: {
      marginLeft: -12,
      marginRight: 20
    },
    actions: {
      height: 20,
      marginTop: -15,
      marginLeft: -18
    },
    action: {
      fontSize: 17,
      color: '#a0a0a0',
      width: 30,
      height: 30,
      marginRight: 3,
      marginLeft: 3,
      '&:hover': {
        [`&.${CONTENTS_IDS.info}`]: {
          color: theme.palette.info[500]
        },
        [`&.${CONTENTS_IDS.pinned}`]: {
          color: theme.palette.danger[500]
        },
        [`&.${CONTENTS_IDS.files}`]: {
          color: theme.palette.warning[500]
        },
        [`&.${CONTENTS_IDS.members}`]: {
          color: theme.palette.success[500]
        }
      }
    },
    actionWithSeparator: {
      '&::after': {
        display: 'block',
        position: 'absolute',
        top: '50%',
        right: 'auto',
        bottom: 'auto',
        left: -4,
        height: 17,
        transform: 'translateY(-50%)',
        borderRadius: 0,
        borderRight: '1px solid #e5e5e5',
        content: '""',
        color: '#2c2d30'
      }
    },
    actionActive: {
      [`&.${CONTENTS_IDS.info}`]: {
        color: theme.palette.info[500]
      },
      [`&.${CONTENTS_IDS.pinned}`]: {
        color: theme.palette.danger[500]
      },
      [`&.${CONTENTS_IDS.files}`]: {
        color: theme.palette.warning[500]
      },
      [`&.${CONTENTS_IDS.members}`]: {
        color: theme.palette.success[500]
      }
    },
    searchContainer: {
      paddingLeft: 5
    }
  };
};

class NavBar extends React.Component {
  handlePinned = () => {
    return this.openRight(CONTENTS_IDS.pinned);
  };

  handleFiles = () => {
    return this.openRight(CONTENTS_IDS.files);
  };

  handleMembers = () => {
    return this.openRight(CONTENTS_IDS.members);
  };

  handleInfo = () => {
    return this.openRight(CONTENTS_IDS.info);
  };

  openRight = (id, props) => {
    this.props.updateChatAppRight({ open: true, componentId: id, props: props });
    return false;
  };

  handleClose = () => {
    goTo(get('root'));
    this.props.closeChatApp({ drawer: true });
    return false;
  };

  handelSearch = (filter) => {
    return this.openRight(CONTENTS_IDS.search, { filter: filter });
  };

  handleSearchCancel = () => {
    this.props.updateChatAppRight({ open: false, componentId: null, props: {}, full: false });
    return false;
  };

  render() {
    const { data, classes, rightOpen, rightFull, rightComponentId, className } = this.props;
    const isBackground = rightOpen && rightFull && rightComponentId === CONTENTS_IDS.reply;
    const channel = data.channel;
    const actionWithSeparator = classNames(classes.action, classes.actionWithSeparator);
    const searchFormId = getFormId('channel-search-form');
    const channelTitle = channel && channel.title;
    return (
      <ShortcutsManager domain="CHATAPP" shortcuts={{ CHATAPP_CLOSE: this.handleClose, CHATAPP_INFO: this.handleInfo }}>
        <AppBar className={classNames(className, classes.appBar)} color="inherit">
          <Toolbar>
            <Hidden mdUp>
              <IconButton
                className={classes.menuButton}
                color="primary"
                aria-label="Menu"
                onClick={() => {
                  this.props.openDrawer('chatApp');
                }}
              >
                <ChatIcon />
              </IconButton>
            </Hidden>
            <Typography type="title" color="inherit" className={classes.titleContainer}>
              <div className={classNames(classes.title, { [classes.titleBackground]: isBackground })}>
                <Icon className={classNames('mdi-set mdi-pound', classes.icon, { [classes.titleBackground]: isBackground })} />
                {channelTitle}
              </div>
              <CardActions className={classes.actions} disableActionSpacing>
                <OverlaidTooltip tooltip={I18n.t('channels.navbar.pinned')} placement="bottom">
                  <IconButton
                    onClick={this.handlePinned}
                    className={classNames(CONTENTS_IDS.pinned, classes.action, {
                      [classes.actionActive]: rightComponentId === CONTENTS_IDS.pinned
                    })}
                  >
                    <Icon className="mdi-set mdi-pin" />
                  </IconButton>
                </OverlaidTooltip>
                <OverlaidTooltip tooltip={I18n.t('channels.navbar.files')} placement="bottom">
                  <IconButton
                    onClick={this.handleFiles}
                    className={classNames(CONTENTS_IDS.files, actionWithSeparator, {
                      [classes.actionActive]: rightComponentId === CONTENTS_IDS.files
                    })}
                  >
                    <Icon className={classNames('mdi-set mdi-file-outline', classes.filesIcon)} />
                  </IconButton>
                </OverlaidTooltip>
                <OverlaidTooltip tooltip={I18n.t('channels.navbar.members')} placement="bottom">
                  <IconButton
                    onClick={this.handleMembers}
                    className={classNames(CONTENTS_IDS.members, actionWithSeparator, {
                      [classes.actionActive]: rightComponentId === CONTENTS_IDS.members
                    })}
                  >
                    <Icon className={classNames('mdi-set mdi-account-multiple-outline', classes.membersIcon)} />
                  </IconButton>
                </OverlaidTooltip>
              </CardActions>
            </Typography>
            <div className={classes.menuContainer}>
              <OverlaidTooltip tooltip={I18n.t('channels.navbar.info')} placement="bottom">
                <IconButton
                  onClick={this.handleInfo}
                  className={classNames(CONTENTS_IDS.info, classes.action, {
                    [classes.actionActive]: rightComponentId === CONTENTS_IDS.info
                  })}
                >
                  <InfoOutlineIcon className={classes.infoIcon} />
                </IconButton>
              </OverlaidTooltip>
              <div className={classes.search}>
                <Search
                  form={searchFormId}
                  key={searchFormId}
                  onSearch={this.handelSearch}
                  onCancel={this.handleSearchCancel}
                  title={<Translate value="forms.comment.searchPlaceholder" name={channelTitle || '...'} />}
                  classes={{ container: classes.searchContainer }}
                />
              </div>
            </div>
            <IconButton color="primary" aria-label="Menu" onClick={this.handleClose}>
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
      </ShortcutsManager>
    );
  }
}

export const mapDispatchToProps = {
  updateChatAppRight: updateChatAppRight,
  closeChatApp: closeChatApp,
  openDrawer: openDrawer
};

export const mapStateToProps = (state) => {
  return {
    rightComponentId: state.apps.chatApp.right.componentId,
    rightFull: state.apps.chatApp.right.full,
    rightOpen: state.apps.chatApp.right.open
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(NavBar)
);