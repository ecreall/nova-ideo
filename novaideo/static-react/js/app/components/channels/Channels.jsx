import React from 'react';
import { withStyles } from 'material-ui/styles';
import Divider from 'material-ui/Divider';
import { ListItem, ListItemText } from 'material-ui/List';

import PrivateChannels from './PrivateChannels';
import PublicChannels from './PublicChannels';

const styles = {
  list: {
    width: 220,
    height: '100%'
  },
  channelBlokTitle: {
    color: 'white',
    fontSize: 14
  }
};

class Channels extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.list}>
        <ListItem>
          <ListItemText classes={{ text: classes.channelBlokTitle }} primary="Channels" />
        </ListItem>
        <PublicChannels
          listStyle={{
            height: '50%'
          }}
        />
        <Divider light />
        <ListItem>
          <ListItemText classes={{ text: classes.channelBlokTitle }} primary="Private" />
        </ListItem>
        <PrivateChannels
          listStyle={{
            height: '50%'
          }}
        />
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Channels);