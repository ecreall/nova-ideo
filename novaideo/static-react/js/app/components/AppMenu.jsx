import React from 'react';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Divider from 'material-ui/Divider';
import InboxIcon from 'material-ui-icons/Inbox';
import { STYLE_CONST } from '../constants';

const styles = {
  list: {
    width: STYLE_CONST.drawerWidth
  }
};

class AppMenu extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.list}>
        <List>
          <ListItem button>
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary="Inbox" />
          </ListItem>
        </List>
        <Divider />
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(AppMenu);