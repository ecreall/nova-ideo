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

import { updateApp } from '../../actions/actions';

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
    marginBottom: 10
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
    height: 0,
    marginTop: 5,
    marginLeft: -18
  },
  action: {
    fontSize: 18,
    color: '#a0a0a0'
  }
};

class NavBar extends React.Component {
  render() {
    const { data, classes, className, updateChatApp } = this.props;
    const channel = data.channel;
    return (
      <AppBar className={classNames(className, classes.appBar)} color="inherit">
        <Toolbar>
          <Typography type="title" color="inherit" className={classes.titleContainer}>
            <div className={classes.title}>
              <Icon className={classNames('mdi-set mdi-pound', classes.icon)} />
              {channel && channel.title}
            </div>
            <CardActions className={classes.actions} disableActionSpacing>
              <IconButton
                onClick={() => {
                  return updateChatApp('chatApp', { right: { open: true, componentId: 'idea' } });
                }}
                className={classes.action}
                aria-label="Add to favorites"
              >
                <VisibilityIcon />
              </IconButton>
            </CardActions>
          </Typography>
          <IconButton
            className={classes.menuButton}
            color="primary"
            aria-label="Menu"
            onClick={() => {
              return updateChatApp('chatApp', { open: false });
            }}
          >
            <CloseIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
    );
  }
}

export const mapDispatchToProps = {
  updateChatApp: updateApp
};

export const mapStateToProps = (state) => {
  return {
    channelsDrawer: state.apps.chatApp.drawer
  };
};
export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(NavBar));