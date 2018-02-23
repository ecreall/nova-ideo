import React from 'react';
import classNames from 'classnames';
import { Translate } from 'react-redux-i18n';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Icon from 'material-ui/Icon';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import InfoOutlineIcon from 'material-ui-icons/InfoOutline';
import CloseIcon from 'material-ui-icons/Close';
import { connect } from 'react-redux';
import { CardActions } from 'material-ui/Card';
import ChatIcon from 'material-ui-icons/Chat';
import Hidden from 'material-ui/Hidden';
import InsertDriveFileIcon from 'material-ui-icons/InsertDriveFile';

import { updateApp, closeChatApp } from '../../actions/actions';
import ShortcutsManager from '../common/ShortcutsManager';
import { goTo, get } from '../../utils/routeMap';
import { CONTENTS_IDS } from './chatAppRight';
import Search from '../forms/Search';

const styles = {
  root: {
    width: '100%'
  },
  menuContainer: {
    display: 'flex',
    alignItems: 'center',
    height: 34,
    margin: '2px 0 0',
    padding: '0 10px 0 0',
    width: 350,
    transition: 'width .15s ease-out 0s',
    '&:focus-within': {
      width: 400
    }
  },
  titleContainer: {
    flex: 1,
    color: '#2c2d30',
    fontSize: 18,
    fontWeight: 900
  },
  title: {
    marginBottom: 19
  },
  icon: {
    color: '#2c2d30',
    fontWeight: 900
  },
  bigIcon: {
    fontSize: '21px !important'
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
    fontSize: 18,
    color: '#a0a0a0'
  },
  actionWithSeparator: {
    '&::after': {
      display: 'block',
      position: 'absolute',
      top: '50%',
      right: 'auto',
      bottom: 'auto',
      left: -1,
      height: 20,
      transform: 'translateY(-50%)',
      borderRadius: 0,
      borderRight: '1px solid #e5e5e5',
      content: '""',
      color: '#2c2d30'
    }
  }
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
    this.props.updateApp('chatApp', { right: { open: true, componentId: id, props: props } });
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
    this.props.updateApp('chatApp', { right: { open: false, componentId: null, props: null } });
    return false;
  };

  render() {
    const { data, classes, className } = this.props;
    const channel = data.channel;
    const actionWithSeparator = classNames(classes.action, classes.actionWithSeparator);
    const searchFormId = 'channel-search-form';
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
                  this.props.updateApp('drawer', { open: true, app: 'chatApp' });
                }}
              >
                <ChatIcon />
              </IconButton>
            </Hidden>
            <Typography type="title" color="inherit" className={classes.titleContainer}>
              <div className={classes.title}>
                <Icon className={classNames('mdi-set mdi-pound', classes.icon)} />
                {channelTitle}
              </div>
              <CardActions className={classes.actions} disableActionSpacing>
                <IconButton onClick={this.handleInfo} className={classes.action}>
                  <InfoOutlineIcon />
                </IconButton>
                <IconButton onClick={this.handleMembers} className={actionWithSeparator}>
                  <Icon className={classNames('mdi-set mdi-account-multiple-outline', classes.bigIcon)} />
                </IconButton>
                <IconButton onClick={this.handlePinned} className={actionWithSeparator}>
                  <Icon className="mdi-set mdi-pin" />
                </IconButton>
                <IconButton onClick={this.handleFiles} className={actionWithSeparator}>
                  <InsertDriveFileIcon />
                </IconButton>
              </CardActions>
            </Typography>
            <div className={classes.menuContainer}>
              <Search
                form={searchFormId}
                key={searchFormId}
                onSearch={this.handelSearch}
                onCancel={this.handleSearchCancel}
                title={<Translate value="forms.comment.searchPlaceholder" name={channelTitle || '...'} />}
              />
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
  updateApp: updateApp,
  closeChatApp: closeChatApp
};

export const mapStateToProps = (state) => {
  return {
    previousLocation: state.history.navigation.previous
  };
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(NavBar));