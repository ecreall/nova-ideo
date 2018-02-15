import React from 'react';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Icon from 'material-ui/Icon';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import CloseIcon from 'material-ui-icons/Close';
import { connect } from 'react-redux';
import { CardActions } from 'material-ui/Card';
import VisibilityIcon from 'material-ui-icons/Visibility';
import ChatIcon from 'material-ui-icons/Chat';
import Hidden from 'material-ui/Hidden';

import { updateApp, closeChatApp } from '../../actions/actions';
import ShortcutsManager from '../common/ShortcutsManager';
import { goTo, get } from '../../utils/routeMap';

const styles = {
  root: {
    width: '100%'
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
  icon: {
    color: '#2c2d30',
    fontWeight: 900
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
  }
};

class NavBar extends React.Component {
  handleInfo = () => {
    this.props.updateApp('chatApp', { right: { open: true, componentId: 'info' } });
    return false;
  };

  handleClose = () => {
    goTo(get('root'));
    this.props.closeChatApp({ drawer: true });
    return false;
  };

  render() {
    const { data, classes, className } = this.props;
    const channel = data.channel;
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
                {channel && channel.title}
              </div>
              <CardActions className={classes.actions} disableActionSpacing>
                <IconButton onClick={this.handleInfo} className={classes.action} aria-label="Add to favorites">
                  <VisibilityIcon />
                </IconButton>
              </CardActions>
            </Typography>
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