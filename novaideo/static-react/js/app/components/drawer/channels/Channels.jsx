import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';
import { I18n } from 'react-redux-i18n';

import PrivateChannels from './PrivateChannels';
import PublicChannels from './PublicChannels';
import { STYLE_CONST } from '../../../constants';

const styles = (theme) => {
  return {
    list: {
      display: 'flex',
      flexDirection: 'column',
      width: STYLE_CONST.drawerWidth,
      height: '100%',
      marginTop: 15
    },
    titleContainer: {
      padding: '0 12px 0 15px',
      width: '100%',
      height: 26,
      color: theme.palette.primary.light,
      fontSize: 16,
      marginBottom: 2
    },
    title: {
      display: 'flex',
      alignItems: 'center'
    },
    divider: {
      marginBottom: 20
    }
  };
};

export const DumbChannels = ({ classes }) => {
  return (
    <div className={classes.list}>
      <div className={classes.titleContainer}>
        <div className={classes.title}>
          {I18n.t('channels.channels')}
        </div>
      </div>
      <PublicChannels />
      <Divider className={classes.divider} light />
      <div className={classes.titleContainer}>
        <div className={classes.title}>
          {I18n.t('channels.private')}
        </div>
      </div>
      <PrivateChannels />
    </div>
  );
};

export default withStyles(styles, { withTheme: true })(DumbChannels);