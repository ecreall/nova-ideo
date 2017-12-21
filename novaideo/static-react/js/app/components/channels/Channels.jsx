import React from 'react';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Divider from 'material-ui/Divider';
import InboxIcon from 'material-ui-icons/Inbox';

import FullScreenDialog from './ChannelDialog';

const styles = (theme) => {
  return {
    icon: { color: theme.palette.primary['50'] },
    text: {
      color: theme.palette.primary['50']
    },
    list: {
      width: 220
    }
  };
};

class Channels extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.list}>
        <List>
          <ListItem button>
            <ListItemIcon>
              <InboxIcon className={classes.icon} />
            </ListItemIcon>
            <ListItemText className={{ root: classes.text }} primary="Inbox" />
          </ListItem>
        </List>
        <Divider />
        <FullScreenDialog />
        <FullScreenDialog />
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Channels);