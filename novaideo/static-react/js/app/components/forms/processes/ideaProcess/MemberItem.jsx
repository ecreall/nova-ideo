/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import ListItemText from '@material-ui/core/ListItemText';
import classNames from 'classnames';

import UserAvatar from '../../../user/UserAvatar';

const styles = (theme) => {
  return {
    text: {
      fontSize: 15,
      padding: 0,
      whiteSpace: 'nowrap',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      fontWeight: 600
    },
    textSelected: {
      color: theme.palette.tertiary.hover.color,
      '&:hover': {
        color: theme.palette.tertiary.hover.color
      }
    },
    avatar: {
      width: 27,
      height: 27,
      marginRight: 7,
      borderRadius: 4
    },
    avatarNoPicture: {
      fontSize: 17,
      backgroundColor: theme.palette.primary['500'],
      color: 'white'
    }
  };
};

export class DumbMemberItem extends React.PureComponent {
  render() {
    const { classes, node, isSelected } = this.props;
    const { title, picture } = node;
    const textClasses = classNames('menu-item-text', classes.text, { [classes.textSelected]: isSelected });
    return (
      <React.Fragment>
        <UserAvatar
          picture={picture}
          classes={{ avatar: classes.avatar, noPicture: classes.avatarNoPicture }}
          title={node.title}
        />
        <ListItemText classes={{ primary: textClasses }} className={textClasses} primary={title} />
      </React.Fragment>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbMemberItem);