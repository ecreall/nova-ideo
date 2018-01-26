import React from 'react';
import { withStyles } from 'material-ui/styles';
import Divider from 'material-ui/Divider';
import { ListItem, ListItemText } from 'material-ui/List';
import { I18n } from 'react-redux-i18n';

import PrivateChannels from './PrivateChannels';
import PublicChannels from './PublicChannels';

const styles = (theme) => {
  return {
    list: {
      display: 'flex',
      flexDirection: 'column',
      width: 220,
      height: '100%',
      marginTop: 20
    },
    channelBlokTitle: {
      color: theme.palette.primary.light,
      fontSize: 16
    },
    publicContainer: {
      marginBottom: 2
    },
    privateContainer: {
      marginTop: 20,
      marginBottom: 2
    }
  };
};

class Channels extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.list}>
        <ListItem classes={{ root: classes.publicContainer }}>
          <ListItemText classes={{ text: classes.channelBlokTitle }} primary={I18n.t('channels.channels')} />
        </ListItem>
        <PublicChannels />
        <Divider light />
        <ListItem classes={{ root: classes.privateContainer }}>
          <ListItemText classes={{ text: classes.channelBlokTitle }} primary={I18n.t('channels.private')} />
        </ListItem>
        <PrivateChannels />
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Channels);