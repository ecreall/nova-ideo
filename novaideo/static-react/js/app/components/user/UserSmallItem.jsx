/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';

import UserTitle from './UserTitle';
import UserAvatar from './UserAvatar';

const styles = {
  container: {
    display: 'flex',
    alignItems: 'center',
    background: 'white',
    padding: 10
  },
  title: {
    fontWeight: 700
  },
  avatar: {
    width: 24,
    height: 24,
    marginRight: 7,
    borderRadius: 4
  },
  avatarNoPicture: {
    fontSize: 11
  }
};

export const DumbUserSmallItem = ({ node, classes }) => {
  return (
    <div className={classes.container}>
      <UserAvatar
        isAnonymous={node.isAnonymous}
        picture={node.picture}
        title={node.title}
        classes={{ avatar: classes.avatar, noPicture: classes.avatarNoPicture }}
      />
      <UserTitle
        node={node}
        classes={{
          title: classes.title
        }}
      />
    </div>
  );
};

export default withStyles(styles)(DumbUserSmallItem);