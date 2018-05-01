import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

import { iconAdapter } from '../../utils/globalFunctions';

const styles = (theme) => {
  return {
    container: {
      padding: 16,
      border: '1px solid #e8e8e8',
      background: '#fff',
      color: '#2c2d30',
      borderLeftWidth: 5,
      borderRadius: 6,
      display: 'flex',
      '&.info': {
        borderLeftColor: theme.palette.info[500]
      },
      '&.danger': {
        borderLeftColor: theme.palette.danger.primary
      },
      '&.warning': {
        borderLeftColor: theme.palette.warning[500]
      },
      '&.success': {
        borderLeftColor: theme.palette.success[500]
      }
    },
    icon: {
      marginRight: 10,
      fontSize: '22px !important',
      marginTop: -7,
      '&.info': {
        color: theme.palette.info[500]
      },
      '&.danger': {
        color: theme.palette.danger.primary
      },
      '&.warning': {
        color: theme.palette.warning[500]
      },
      '&.success': {
        color: theme.palette.success[500]
      }
    }
  };
};

export const ALERTS_ICONS = {
  info: iconAdapter('mdi-set mdi-alert-circle-outline'),
  danger: iconAdapter('mdi-set mdi-alert-outline'),
  warning: iconAdapter('mdi-set mdi-alert-box'),
  success: iconAdapter('mdi-set mdi-check-circle-outline')
};

export const DumbAlert = ({ type = 'info', classes, children }) => {
  const Icon = ALERTS_ICONS[type];
  return (
    <div className={classNames(classes.container, type)}>
      <Icon className={classNames(classes.icon, type)} />
      <div>
        {children}
      </div>
    </div>
  );
};

export default withStyles(styles, { withTheme: true })(DumbAlert);