/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { ListItem, ListItemIcon, ListItemSecondaryAction, ListItemText } from 'material-ui/List';
import Icon from 'material-ui/Icon';
import CreateIcon from 'material-ui-icons/Create';
import Badge from 'material-ui/Badge';
import { connect } from 'react-redux';
import classNames from 'classnames';
import { red } from 'material-ui/colors';

import { goTo, get } from '../../utils/routeMap';
import UserAvatar from '../user/UserAvatar';

const styles = (theme) => {
  return {
    listItem: {
      paddingTop: 4,
      paddingBottom: 4
    },
    listItemActive: {
      backgroundColor: theme.palette.tertiary.color,
      '&:hover': {
        backgroundColor: theme.palette.tertiary.color
      }
    },
    text: {
      color: 'white',
      fontSize: 15,
      opacity: 0.8,
      padding: 0,
      whiteSpace: 'nowrap',
      textOverflow: 'ellipsis',
      overflow: 'hidden'
    },
    textActive: {
      opacity: 1,
      fontWeight: '700'
    },
    textSelected: {
      color: theme.palette.tertiary.hover.color,
      '&:hover': {
        color: theme.palette.tertiary.hover.color
      }
    },
    icon: {
      width: 17,
      height: 15,
      color: 'white',
      opacity: 0.4,
      marginRight: 0,
      fontSize: '12px !important'
    },
    iconActive: {
      opacity: 1
    },
    iconSelected: {
      color: theme.palette.tertiary.hover.color,
      '&:hover': {
        color: theme.palette.tertiary.hover.color
      }
    },
    avatar: {
      width: 18,
      height: 18,
      marginRight: 7,
      borderRadius: 4
    },
    avatarNoPicture: {
      fontSize: 11,
      backgroundColor: 'white',
      color: theme.palette.primary['500']
    },
    badge: {
      right: 15,
      marginTop: -11,
      fontWeight: '700'
    },
    badgeColor: {
      color: 'white',
      backgroundColor: red['500'],
      padding: '5px 9px',
      marginLeft: 4,
      borderRadius: '1em',
      fontSize: 12,
      fontWeight: 700,
      width: 'auto',
      height: 'auto',
      top: -11
    },
    unreadComment: {
      color: 'white',
      fontWeight: '700'
    }
  };
};

export class DumbChannelItem extends React.Component {
  open = () => {
    goTo(get('messages', { channelId: this.props.node.id }));
  };

  renderIcon = (isActive, isSelected) => {
    const { classes, node, itemProps, currentMessage } = this.props;
    const channelPicture = node.subject.picture;
    const hasMessage = currentMessage && currentMessage.values && currentMessage.values.comment;
    if (!isSelected && hasMessage) {
      return (
        <ListItemIcon>
          <CreateIcon
            className={classNames(classes.icon, {
              [classes.iconActive]: isActive,
              [classes.iconSelected]: isSelected
            })}
          />
        </ListItemIcon>
      );
    }
    return itemProps && itemProps.isDiscussion
      ? <UserAvatar
        picture={channelPicture}
        classes={{ avatar: classes.avatar, noPicture: classes.avatarNoPicture }}
        title={node.title}
      />
      : <ListItemIcon>
        <Icon
          className={classNames('mdi-set mdi-pound', classes.icon, {
            [classes.iconActive]: isActive,
            [classes.iconSelected]: isSelected
          })}
        />
      </ListItemIcon>;
  };
  render() {
    const { classes, node, activeChannel } = this.props;
    const lenUnreadComments = node.unreadComments.length;
    const hasUnread = lenUnreadComments > 0;
    const isSelected = activeChannel === node.id;
    const isActive = isSelected || hasUnread;
    const textClasses = classNames(classes.text, { [classes.textActive]: isActive, [classes.textSelected]: isSelected });
    return (
      <ListItem
        onClick={this.open}
        dense
        button
        classes={{ root: classNames(classes.listItem, { [classes.listItemActive]: isSelected }) }}
      >
        {this.renderIcon(isActive, isSelected)}
        <ListItemText classes={{ primary: textClasses }} className={textClasses} primary={node.title} />
        {hasUnread &&
          <ListItemSecondaryAction className={classes.badge}>
            <Badge classes={{ colorAccent: classes.badgeColor }} badgeContent={lenUnreadComments} color="accent" />
          </ListItemSecondaryAction>}
      </ListItem>
    );
  }
}

export const mapStateToProps = (state, props) => {
  return {
    currentMessage: state.form[props.node.id],
    activeChannel: state.apps.chatApp.channel
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(DumbChannelItem));