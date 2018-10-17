import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import IconButton from '@material-ui/core/IconButton';

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
      alignItems: 'center',
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
    },
    closeBtn: {
      fontSize: 18,
      height: 35,
      width: 35,
      marginLeft: 10,
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

export class DumbAlert extends React.Component {
  static defaultProps = {
    type: 'info'
  };

  state = {
    open: true
  };

  close = () => {
    this.setState({ open: false });
  };

  render() {
    const {
      type, dismissible, classes, children
    } = this.props;
    const { open } = this.state;
    const Icon = ALERTS_ICONS[type];
    const CloseIcon = iconAdapter('mdi-set mdi-close');
    const isOpen = (dismissible && open) || !dismissible;
    return (
      isOpen && (
        <div className={classNames(classes.container, type)}>
          <Icon className={classNames(classes.icon, type)} />
          <div className={classes.messageContainer}>{children}</div>
          {dismissible && (
            <IconButton className={classNames(classes.closeBtn, type)} onClick={this.close}>
              <CloseIcon />
            </IconButton>
          )}
        </div>
      )
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbAlert);