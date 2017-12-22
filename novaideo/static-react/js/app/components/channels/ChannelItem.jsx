/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { ListItem, ListItemIcon, ListItemSecondaryAction, ListItemText } from 'material-ui/List';
import WifiIcon from 'material-ui-icons/Wifi';
import Badge from 'material-ui/Badge';
import { connect } from 'react-redux';
import Avatar from 'material-ui/Avatar';
import classNames from 'classnames';
import { red } from 'material-ui/colors';

import { updateApp } from '../../actions/actions';

const styles = (theme) => {
  return {
    listItemActive: {
      backgroundColor: 'white',
      '&:hover': {
        backgroundColor: 'white'
      }
    },
    text: {
      color: 'white',
      fontSize: 13,
      opacity: 0.8,
      padding: 0
    },
    textActive: {
      opacity: 1,
      fontWeight: 'bold'
    },
    textSelected: {
      color: theme.palette.primary['500'],
      '&:hover': {
        color: theme.palette.primary['500']
      }
    },
    icon: {
      width: 17,
      color: 'white',
      opacity: 0.7
    },
    iconActive: {
      opacity: 1
    },
    iconSelected: {
      color: theme.palette.primary['500'],
      '&:hover': {
        color: theme.palette.primary['500']
      }
    },
    avatar: {
      width: 20,
      height: 20,
      marginRight: 10
    },
    badge: {
      right: 15,
      marginTop: -15,
      fontWeight: 'bold'
    },
    badgeColor: {
      color: 'white',
      backgroundColor: red['500']
    },
    unreadComment: {
      color: 'white',
      fontWeight: 'bold'
    }
  };
};

export class DumbChannelItem extends React.Component {
  handleClickOpen = () => {
    const { openChannel, node } = this.props;
    this.setState({ open: true }, () => {
      return openChannel('chatApp', { open: true, channel: node.id });
    });
  };
  render() {
    const { classes, node, itemdata, activeChannel } = this.props;
    const channelPicture = node.subject.picture;
    const lenUnreadComments = node.unreadComments.length;
    const hasUnread = lenUnreadComments > 0;
    const isSelected = activeChannel === node.id;
    const isActive = isSelected || hasUnread;
    const textClasses = classNames(classes.text, { [classes.textActive]: isActive, [classes.textSelected]: isSelected });
    return (
      <ListItem onClick={this.handleClickOpen} dense button classes={isSelected && { root: classes.listItemActive }}>
        {itemdata && itemdata.isDiscussion
          ? <Avatar className={classes.avatar} src={channelPicture ? `${channelPicture.url}/profil` : ''} />
          : <ListItemIcon>
            <WifiIcon
              className={classNames(classes.icon, { [classes.iconActive]: isActive, [classes.iconSelected]: isSelected })}
            />
          </ListItemIcon>}
        <ListItemText classes={{ text: textClasses }} className={textClasses} primary={node.title} />
        {hasUnread &&
          <ListItemSecondaryAction className={classes.badge}>
            <Badge classes={{ colorAccent: classes.badgeColor }} badgeContent={lenUnreadComments} color="accent" />
          </ListItemSecondaryAction>}
      </ListItem>
    );
  }
}

export const mapDispatchToProps = {
  openChannel: updateApp
};

export const mapStateToProps = (state) => {
  return {
    activeChannel: state.apps.chatApp.channel
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(DumbChannelItem));